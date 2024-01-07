from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User


from django.shortcuts import get_object_or_404

from django.utils.safestring import mark_safe

from .models import UserSkill, UserSkillSource, UserRecommendations

from apps.website.models import Skill, Specialization, SpecializationSkills, Field, LearningMaterial
from apps.acad.models import StudentProfile, Course, Curriculum, Subject, StudentGrades
from apps.recommender_survey.models import Survey as RecommenderSurvey
from apps.assessment.models import QuestionSet

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

import os
import plotly.express as px
import plotly.io as pio

# import minmaxscaler
from sklearn.preprocessing import MinMaxScaler
# import tfidf
from sklearn.feature_extraction.text import TfidfTransformer

def load_csv(request):
    csv_file_name = 'field_skills_tfidf.csv'
    csv_file_path = os.path.join(os.path.dirname(__file__), csv_file_name)

    try:
        # Read the CSV file into a DataFrame
        specialization_sparse = pd.read_csv(csv_file_path)
        # Process the DataFrame as needed (e.g., save to the database, perform operations)
        return specialization_sparse
    except Exception as e:
        #print("Error processing file: {}".format(e))
        # empty DataFrame with the same columns and dtypes as your original DataFrame
        specialization_sparse = pd.DataFrame()
        return specialization_sparse



def get_user_skills(request):
    user_skills = UserSkill.objects.filter(user=request.user)
    user_skills_list = [skill.skill.skill for skill in user_skills]
    return list(set(user_skills_list))

def get_intersection_columns(user_skills_list, normalized_field_skills):
    normalized_field_skills_columns = list(normalized_field_skills.columns)
    return list(set(user_skills_list).intersection(set(normalized_field_skills_columns)))

def create_skill_plot(user_skills_df):
    fig = px.bar(
        user_skills_df,
        x='level',
        y='field',
        barmode ='stack',
        hover_data=['skill'],
        orientation='h',
        labels={'level': 'Count', 'field': 'Field'},
        #color_discrete_sequence=list(field_dict.values()),
        color='field',
    )

    # x and y title
    #fig.update_xaxes(title_text='Skill Level')
    #fig.update_yaxes(title_text='Skill Name')
    fig.update_xaxes(title_text='Count')
    fig.update_yaxes(title_text='Field')
    skill_plot = pio.to_html(fig, full_html=False)
    return skill_plot

def create_field_plot(fields_df):
     # Create a pie chart using Plotly Express
    fig = px.pie(fields_df, values='Score', names='Field_Name',
                 #title='Top Field Recommendation Score'
                 )
    # set title
    #fig.update_layout(title_text='Top Field Recommendation Score', title_x=0.5)

    # remove white background
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    # Convert the figure to HTML
    field_plot = pio.to_html(fig, full_html=False)
    return field_plot


def create_stacked_skills(normalized_copy):
    stacked_skills = px.bar(
        normalized_copy, 
        x='level', 
        y='field_name', 
        color='field_name', 
        # title='Skills Levels',
        orientation='h',
        labels={'level': 'Relevance Score',  'skill': 'Skill'}, #'field_name': 'Field Name',
        color_continuous_scale=px.colors.sequential.Plasma,
        height=500,
        width=800,
    )

    # convert to html
    stacked_skills = pio.to_html(stacked_skills, full_html=False)
    return stacked_skills

def create_radar_skills(normalized_copy):
    # create the radar chart
    radar_skills = px.line_polar(
        normalized_copy, 
        r='level', 
        theta='skill', 
        color='field_name', 
        line_close=True,
        # title='Skills Levels',
        labels={'level': 'Relevance Score', 'field_name': 'Field Name'},
        #color_continuous_scale=px.colors.sequential.Plasma,
        height=500,
        width=800,
    )
    radar_skills = pio.to_html(radar_skills, full_html=False)
    return radar_skills

def save_user_recommendation(request, top_3_fields, top_3_fields_score):
        # get StudentProfile year
    student_year = StudentProfile.objects.get(user=request.user).current_year

    #UserRecommendations get or create
    user_recommendations = UserRecommendations.objects.get_or_create(user=request.user, current_year=student_year)[0]

    user_recommendations.field_1 = Field.objects.get(field=top_3_fields[0])
    user_recommendations.field_2 = Field.objects.get(field=top_3_fields[1])
    user_recommendations.field_3 = Field.objects.get(field=top_3_fields[2])
    user_recommendations.score_1 = float(top_3_fields_score[0])
    user_recommendations.score_2 = float(top_3_fields_score[1])
    user_recommendations.score_3 = float(top_3_fields_score[2])


    user_recommendations.save()

def recommender(request):
    # Get the user's skills from the request.
    user_skills_list = get_user_skills(request)
    normalized_field_skills = load_csv(request)
    intersection_columns = get_intersection_columns(user_skills_list, normalized_field_skills)

    if len(intersection_columns) == 0:
        return render(request, 'recommender/recommender_failed.html')


    # get level of each skill
    user_skills_level = []
    for skill in intersection_columns:
        userskill_level = UserSkill.objects.get(user=request.user, skill__skill=skill).level
        user_skills_level.append(userskill_level)


    user_skills_dict = dict(zip(intersection_columns, user_skills_level))   
    user_skills_df = pd.DataFrame.from_dict(user_skills_dict, orient='index').T

    # use tfidf
    tfidf = TfidfTransformer()
    normalized_user_skills_df = pd.DataFrame(tfidf.fit_transform(user_skills_df).toarray(), columns=user_skills_df.columns, index=user_skills_df.index)

    # Filter the specialization data frame columns by the user's skills. except the first and second columns
    normalized_field_skills_filtered = normalized_field_skills[['field_id'] + intersection_columns]
    normalized_field_skills_filtered = normalized_field_skills_filtered[(normalized_field_skills_filtered[intersection_columns] != 0).any(axis=1)]


    cosine_similarities = cosine_similarity(normalized_user_skills_df[intersection_columns], normalized_field_skills_filtered[intersection_columns])
    #print('cosine_similarities: ', cosine_similarities)
    top_3_indices = cosine_similarities.argsort(axis=1)[:, -3:]
    top_3_field = normalized_field_skills_filtered.iloc[:, 0].values[top_3_indices] # rendered
    all_fields = normalized_field_skills_filtered.iloc[:, 0].values
 
    field_ids = normalized_field_skills_filtered['field_id'].unique()
    # Create a dictionary to store the field names and the sum of the cosine similarity scores
    fields_score = {}
    for field_id in all_fields:
        normalized_field_skills_filtered_by_field = normalized_field_skills_filtered[normalized_field_skills_filtered['field_id'] == field_id]
        fields_score[field_id] = normalized_field_skills_filtered_by_field.iloc[:, 1:].sum(axis=1).sum()
    
    # get field names
    fields_name = []
    for field_id in all_fields:
        field_name = Field.objects.get(field=field_id).field_name
        fields_name.append(field_name)

    # should be replace by website_field.id
    field_dict = {
        'Software Development': 1,
        'Data and Analytics': 2,
        'Design and UX/UI': 3,
        'Product Management': 4,
        'Testing and Quality Assurance': 5,
        'Security': 6
    }
    field_dict = {v: k for k, v in field_dict.items()}


    # Calculate the field with the highest matching for each skill
    user_skills_field = []
    field_id_list = []
    for skill in intersection_columns:
        field_id = normalized_field_skills_filtered.loc[normalized_field_skills_filtered[skill].idxmax(), 'field_id']
        field_id_list.append(field_id)
        field = Field.objects.get(field=field_id).field_name
        user_skills_field.append(field)
    
    user_skills_df = pd.DataFrame({
        'skill': intersection_columns,
        'level': user_skills_level,
        'field': user_skills_field,
        'field_id': field_id_list,
    })
    #pivot_df = user_skills_df.pivot(index='skill', columns='field', values='level').fillna(0)

    # user_skills_df['fields_score'] = user_skills_df['field_id'].map(fields_score)
    # user_skills_df = user_skills_df.sort_values('fields_score', ascending=False)
    # user_skills_df = user_skills_df.drop('fields_score', axis=1)

    # skill_plot = create_skill_plot(user_skills_df)
   
    # Create a DataFrame with Field_ID, Field_Name, and Score
    fields_df = pd.DataFrame(list(zip(field_ids, fields_name, fields_score.values())), columns=['Field_ID', 'Field_Name', 'Score'])   
    field_plot = create_field_plot(fields_df)
   

    # # make a copy of normamlied_field
    # normalized_copy = normalized_field_skills_filtered.copy()
    # # label field id of normalized_field_skills_filtered with field_dict
    # normalized_copy['field_name'] = normalized_copy['field_id'].map(field_dict)
    # # melt normalized_field_skills_filtered
    # normalized_copy = normalized_copy.melt(id_vars=['field_id', 'field_name'], var_name='skill', value_name='level')
    # # use fields_score mapping for field_id into field_order
    # normalized_copy['field_order'] = normalized_copy['field_id'].map(fields_score)
    # # sort by field_order
    # normalized_copy = normalized_copy.sort_values('field_order', ascending=False)
    # # remove field_order
    # normalized_copy = normalized_copy.drop('field_order', axis=1)

    #print('normalized_copy: ', normalized_copy)

    # stacked_skills = create_stacked_skills(normalized_copy)

    # radar_skills = create_radar_skills(normalized_copy)

    # Sort the fields by the sum of the cosine similarity scores, in descending order.
    top_3_fields = sorted(fields_score, key=fields_score.get, reverse=True)[:3]
    top_3_fields_score = [fields_score[field_id] for field_id in top_3_fields]

    field_names = []
    for field_id in top_3_fields:
        field_name = Field.objects.get(field=field_id).field_name
        field_names.append(field_name)

    field_name_1 = field_names[0]
    field_name_2 = field_names[1]
    field_name_3 = field_names[2]

    # saving user recommendation
    save_user_recommendation(request, top_3_fields, top_3_fields_score)

    # Roadmap
    # user_reco_step_1 = UserRecommendations.objects.filter(user=request.user, current_year=0).exists()
    # user_reco_step_2 = UserRecommendations.objects.filter(user=request.user, current_year=1).exists()
    # user_reco_step_3 = UserRecommendations.objects.filter(user=request.user, current_year=2).exists()
    # user_reco_step_4 = UserRecommendations.objects.filter(user=request.user, current_year=3).exists()
    # user_reco_step_5 = UserRecommendations.objects.filter(user=request.user, current_year=4).exists()

    return render(request, 'recommender/recommender.html', {
        # Top Results
        'top_3_field_recommendations': top_3_field,
        'field_name_1': field_name_1,
        'field_name_2': field_name_2,
        'field_name_3': field_name_3,
        'field_1': Field.objects.get(field=top_3_fields[0]),
        'field_2': Field.objects.get(field=top_3_fields[1]),
        'field_3': Field.objects.get(field=top_3_fields[2]),
        
        # Plots
        #'skill_plot': skill_plot,           # skill score representation
        'field_plot': field_plot,           # pie graph field recommendation
        #'stacked_skills': stacked_skills,   # skill relevance representation
        #'radar_skills': radar_skills,      # skill relevance representation

        # Roadmap
        # 'step_1': user_reco_step_1,
        # 'step_2': user_reco_step_2,
        # 'step_3': user_reco_step_3,
        # 'step_4': user_reco_step_4,
        # 'step_5': user_reco_step_5,
    })



# def roadmap(request):
#      # Roadmap
#     user_reco_step_1 = UserRecommendations.objects.filter(user=request.user, current_year=0)
#     user_reco_step_2 = UserRecommendations.objects.filter(user=request.user, current_year=1)
#     user_reco_step_3 = UserRecommendations.objects.filter(user=request.user, current_year=2)
#     user_reco_step_4 = UserRecommendations.objects.filter(user=request.user, current_year=3)
#     user_reco_step_5 = UserRecommendations.objects.filter(user=request.user, current_year=4)

#     user_reco_step_1_status = user_reco_step_1.exists()
#     user_reco_step_2_status = user_reco_step_2.exists()
#     user_reco_step_3_status = user_reco_step_3.exists()
#     user_reco_step_4_status = user_reco_step_4.exists()
#     user_reco_step_5_status = user_reco_step_5.exists()

#     # check if it has recommender_survey model survey has user_reco_step_n ID
#     user_survey_s_1_status = RecommenderSurvey.objects.filter(recommendation_id=user_reco_step_1.recommendation_id).exists()
#     user_survey_s_2_status = RecommenderSurvey.objects.filter(recommendation_id=user_reco_step_2.recommendation_id).exists()
#     user_survey_s_3_status = RecommenderSurvey.objects.filter(recommendation_id=user_reco_step_3.recommendation_id).exists()
#     user_survey_s_4_status = RecommenderSurvey.objects.filter(recommendation_id=user_reco_step_4.recommendation_id).exists()
#     user_survey_s_5_status = RecommenderSurvey.objects.filter(recommendation_id=user_reco_step_5.recommendation_id).exists()




#     return render(request, 'recommender/roadmap.html', {
#         # Roadmap
#         'step_1_status': user_reco_step_1_status,
#         'step_2_status': user_reco_step_2_status,
#         'step_3_status': user_reco_step_3_status,
#         'step_4_status': user_reco_step_4_status,
#         'step_5_status': user_reco_step_5_status,

#         # Survey
#         'survey_s_1_status': user_survey_s_1_status,
#         'survey_s_2_status': user_survey_s_2_status,
#         'survey_s_3_status': user_survey_s_3_status,
#         'survey_s_4_status': user_survey_s_4_status,
#         'survey_s_5_status': user_survey_s_5_status,
#     })

def roadmap(request):

    # Roadmap
    user_reco_steps = [UserRecommendations.objects.filter(user=request.user, current_year=i) for i in range(5)]
    user_reco_steps_status = [step.exists() for step in user_reco_steps]
    user_test_status = [QuestionSet.objects.filter(user=request.user, year=i).exists() for i in range(5)]

    # check if it has recommender_survey model survey has user_reco_step_n ID
    user_survey_s_status = []
    for step in user_reco_steps:
        #print(step)
        try:
            status = RecommenderSurvey.objects.filter(recommendation_id=step.first().recommendation_id).exists()
        except AttributeError:
            status = False
        #print(status)
        user_survey_s_status.append(status)

    # get studentprofile
    student_profile = StudentProfile.objects.get(user=request.user)
    student_profile_exists = StudentProfile.objects.filter(user=request.user).exists()
    print("student_profile_exists",student_profile_exists)
    # get course
    course = Course.objects.get(id=student_profile.enrolled_courses_id)
    course_name = course.course_name
    # get course number of years
    user_grade_status = []
    for year in range(1,course.number_of_years+1):
        #first subject from curriculum
        first_subject = Subject.objects.filter(curriculum__course=course, curriculum__year=year).first()
        # on studentgrades check if student_profile.id and subject.id exists
        # if not, return false
        try:
            status = StudentGrades.objects.filter(student_id=student_profile.id, subject_id=first_subject.id).exists()
        except AttributeError:
            status = False
        #print("user grade status {}: {}", year, status)
        user_grade_status.append(status)
        
    step_1_status =  user_reco_steps_status[0] and user_test_status[0]
    step_2_status =  user_reco_steps_status[1] and user_test_status[1] and user_survey_s_status[0] and user_grade_status[0]
    step_3_status =  user_reco_steps_status[2] and user_test_status[2] and user_survey_s_status[1] and user_grade_status[1]
    step_4_status =  user_reco_steps_status[3] and user_test_status[3] and user_survey_s_status[2] and user_grade_status[2]
    step_5_status =  user_reco_steps_status[4] and user_test_status[4] and user_survey_s_status[3] and user_grade_status[3]


    return render(request, 'recommender/roadmap.html', {
        'student_profile_exists': student_profile_exists,
        "course_name": course_name,

        # Roadmap
        'step_1_status': step_1_status,
        'step_2_status': step_2_status,
        'step_3_status': step_3_status,
        'step_4_status': step_4_status,
        'step_5_status': step_5_status,


        # Roadmap
        'reco_1_status': user_reco_steps_status[0],
        'reco_2_status': user_reco_steps_status[1],
        'reco_3_status': user_reco_steps_status[2],
        'reco_4_status': user_reco_steps_status[3],
        'reco_5_status': user_reco_steps_status[4],

        # test
        'test_1_status': user_test_status[0],
        'test_2_status': user_test_status[1],
        'test_3_status': user_test_status[2],
        'test_4_status': user_test_status[3],
        'test_5_status': user_test_status[4],

        # Survey
        'survey_s_1_status': user_survey_s_status[0],
        'survey_s_2_status': user_survey_s_status[1],
        'survey_s_3_status': user_survey_s_status[2],
        'survey_s_4_status': user_survey_s_status[3],
        'survey_s_5_status': user_survey_s_status[4],

        # Grades
        # 'grade_1_status': user_grade_status[0],
        'grade_2_status': user_grade_status[0],
        'grade_3_status': user_grade_status[1],
        'grade_4_status': user_grade_status[2],
        'grade_5_status': user_grade_status[3],
    })
    

def recommendation_field(request, field_id):
    
    field_object = Field.objects.get(field=field_id)
    
    # skills
    user_skills = UserSkill.objects.filter(user=request.user)
    user_skills_list = [skill.skill.skill for skill in user_skills]
    user_skills_list = list(set(user_skills_list))
    user_skills_set = set(user_skills_list)

    # #print('user_skills_list: ', user_skills_list)

    # specialization_skills = SpecializationSkills.objects.filter(specialization__field=field_id)
    # specialization_skills = specialization_skills.filter(skill__skill__in=user_skills_set)

    # # Create a set to store unique skills
    # unique_skills_set = set()

    # # Create a list to store the final unique specialization skills
    # specialization_skills_list = []

    # # Iterate through the specialization skills and filter duplicates
    # for skill in specialization_skills:
    #     skill_name = skill.skill.skill
    #     level = skill.level
    #     # Check if the skill is not in the set to add it
    #     if skill_name not in unique_skills_set:
    #         unique_skills_set.add(skill_name)
    #         specialization_skills_list.append((skill_name, level))

    # # Sort the list by level
    # specialization_skills_list = sorted(specialization_skills_list, key=lambda x: x[1], reverse=True)


    # # filter to 10 only
    # specialization_skills_list = specialization_skills_list[:10]
    # #print('')
    # #print('!!!!specialization_skills: ', specialization_skills_list)
    # # specialization, jobs, roadmap

    normalized_field_skills = load_csv(request)

    #normalized_field_skills_row = normalized_field_skills[normalized_field_skills['field_id'] == field_id]
    # for each skill column get the highest value and only on the field_id = field_id
    # iterate through the columns
    column_list = []
    column_list_2 = []
    # exclude field_id
    for col in normalized_field_skills.columns[1:]:
        # get field id of the highest value
        index_max = normalized_field_skills[col].idxmax()
        # if row_field_id is equal to field_id, get column name
        if normalized_field_skills.loc[index_max, 'field_id'] == field_id:
            column_list.append(col)
        else:
            # if its the second highest value, get the column name
            # get the second highest values field id
            second_highest_field = normalized_field_skills[col].nlargest(2).index[1]
            # if the second highest value's field_id is equal to field_id, get the column name
            if second_highest_field == field_id:
                column_list_2.append(col)

    # filter normalized_field_skills by column_list
    normalized_field_skills_row = normalized_field_skills[['field_id'] + column_list]
    #print(normalized_field_skills_row['field_id'])
    normalized_field_skills_row_2 = normalized_field_skills[['field_id'] + column_list_2]
    # get only row with field_id = field_id
    #print('field_id: ', field_id)
    normalized_field_skills_row = normalized_field_skills_row[normalized_field_skills_row['field_id'] == field_id]
    normalized_field_skills_row_2 = normalized_field_skills_row_2[normalized_field_skills_row_2['field_id'] == field_id]
    #print(normalized_field_skills_row['field_id'])
    # convert to series
    normalized_field_skills_row = normalized_field_skills_row.iloc[:, 1:].sum(axis=0).sort_values(ascending=False)
    normalized_field_skills_row_2 = normalized_field_skills_row_2.iloc[:, 1:].sum(axis=0).sort_values(ascending=False)

    # filter by user skills
    top_user_skills = normalized_field_skills_row[normalized_field_skills_row.index.isin(user_skills_set)]
    top_user_skills = top_user_skills.nlargest(7)
    top_user_skills_2 = normalized_field_skills_row_2[normalized_field_skills_row_2.index.isin(user_skills_set)]
    top_user_skills_2 = top_user_skills_2.nlargest(7)


    # not in user skills
    not_in_user_skills = normalized_field_skills_row[~normalized_field_skills_row.index.isin(user_skills_set)]
    not_in_user_skills = not_in_user_skills.nlargest(7)
    not_in_user_skills_2 = normalized_field_skills_row_2[~normalized_field_skills_row_2.index.isin(user_skills_set)]
    not_in_user_skills_2 = not_in_user_skills_2.nlargest(7)

    # remove 0
    top_user_skills = top_user_skills[top_user_skills != 0]
    top_user_skills_2 = top_user_skills_2[top_user_skills_2 != 0]
    not_in_user_skills = not_in_user_skills[not_in_user_skills != 0]
    not_in_user_skills_2 = not_in_user_skills_2[not_in_user_skills_2 != 0]

    # Get the column names (skills) as a list
    top_user_skills = top_user_skills.index.tolist()
    not_in_user_skills = not_in_user_skills.index.tolist()
    top_user_skills_2 = top_user_skills_2.index.tolist()
    not_in_user_skills_2 = not_in_user_skills_2.index.tolist()

    

    return render(request, 'recommender/recommendation_field.html', {
        'field_object': field_object,
        #'specialization_skills': top_10_skills,
        'top_user_skills': top_user_skills,
        'not_in_user_skills': not_in_user_skills,
        'top_user_skills_2': top_user_skills_2,
        'not_in_user_skills_2': not_in_user_skills_2,
    })


def recommendation_specialization(request, field_id):

    field = Field.objects.get(field=field_id)

    # get specialization
    specialization = Specialization.objects.filter(field=field_id)

    # get specialization skills
    specialization_skills = SpecializationSkills.objects.filter(specialization__field=field_id)

    # get user skills
    user_skills = UserSkill.objects.filter(user=request.user)
    user_skills_list = [skill.skill.skill for skill in user_skills]
    user_skills_list = list(set(user_skills_list))
    user_skills_set = set(user_skills_list)

    # Create a set to store unique skills
    unique_skills_set = set()

    # Create a list to store the final unique specialization skills
    specialization_skills_list = []

    # Iterate through the specialization skills and filter duplicates
    for skill in specialization_skills:
        skill_name = skill.skill.skill
        level = skill.level
        # Check if the skill is not in the set to add it
        if skill_name not in unique_skills_set:
            unique_skills_set.add(skill_name)
            specialization_skills_list.append((skill_name, level))

    # Sort the list by level, get column name
    specialization_skills_list = sorted(specialization_skills_list, key=lambda x: x[1], reverse=True)

    # filter to 10 only
    specialization_skills_list = specialization_skills_list[:10]

    # get specialization jobs
    #specialization_jobs = specialization[0].jobs.all()

    # get specialization roadmap
    #specialization_roadmap = specialization[0].roadmap

    return render(request, 'recommender/recommendation_specialization.html', {
        'field': field,
        'specializations': specialization,
        'specialization': specialization[0],
        'specialization_skills': specialization_skills_list,
        #'specialization_jobs': specialization_jobs,
        #'specialization_roadmap': specialization_roadmap,
    })


def recommendation_course(request, field_id):
    field = Field.objects.get(field=field_id)
    #specialization = Specialization.objects.get(id=specialization_id)
    #roadmap = specialization.roadmap

    learning_materials = LearningMaterial.objects.filter(field_id=field_id)

    try:
        learning_materials_beginner = learning_materials.filter(level='Beginner')
    except:
        learning_materials_beginner = None
    try:
        learning_materials_intermediate = learning_materials.filter(level='Intermediate')
    except:
        learning_materials_intermediate = None
    try:
        learning_materials_advanced = learning_materials.filter(level='Advanced')
    except:
        learning_materials_advanced = None


    return render(request, 'recommender/recommendation_course.html', {
        'field': field,
        #'specialization': specialization,
        #'roadmap': roadmap,
        'learning_materials_beginner': learning_materials_beginner,
        'learning_materials_intermediate': learning_materials_intermediate,
        'learning_materials_advanced': learning_materials_advanced,
    })

# from apps.jobs.models import JobPosting

# def recommendation_jobs(request, field_id, job_id=None):
#     field = Field.objects.get(field=field_id)
    
#     job_postings = JobPosting.objects.filter(field=field_id)
#     selected_job = get_object_or_404(JobPosting, pk=1)   
 
#     if job_id:
#         selected_job = get_object_or_404(JobPosting, pk=job_id)
    

#     selected_job.job_description = mark_safe(selected_job.job_description)

#     return render(request, 'job/job_list.html', {'job_postings': job_postings, 'selected_job': selected_job})
