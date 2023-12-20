from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import LogoutView
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.urls import reverse

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import update_session_auth_hash

#from website.utils import *
from apps.website.forms import SignUpForm, StudentScoreForm
from apps.website.models import Specialization, Field, LearningMaterial
from apps.recommender.models import UserRecommendations, UserSkill

from apps.acad.models import StudentProfile, Course, Subject
from apps.assessment.models import Test, QuestionSet
from apps.jobs.models import JobPosting
from apps.survey.models import Survey

from utilities.decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
# from django.http import FileResponse
# from reportlab.pdfgen import canvas


# from django.http import FileResponse

# from io import BytesIO


# Other Imports
# import json
import logging
# import plotly.express as px
from apps.survey.models import Survey

#logger = logging.getLogger(__name__)
logger = logging.getLogger("django") # name of logger : django


@login_required(login_url='login_user')
#@allowed_users(allowed_roles=['admin','staff','student','instructor']) # only users on the list can access this page, ie. admin and staff
def home(request):
    # logger.debug("User: " + str(request.user) + " is accessing home page")
    # logger.info("User: " + str(request.user) + " is accessing home page")
    # logger.warning("User: " + str(request.user) + " is accessing home page")
    # logger.error("User: " + str(request.user) + " is accessing home page")
    # logger.critical("User: " + str(request.user) + " is accessing home page")

    specialization_items = Specialization.objects.all()
    field_items = Field.objects.all()
    # Fetch user recommendations
    user_recommendations = None
    recommended_fields = None
    #field_items = []
    if request.user.is_authenticated:
        user_recommendations = UserRecommendations.objects.filter(user=request.user).first()

    # Create a list to store the recommended fields
    recommended_fields = []

    # Order recommended fields first
    if user_recommendations:
        recommended_fields.extend([user_recommendations.field_1, user_recommendations.field_2, user_recommendations.field_3])

    print("recommended_fields: ", recommended_fields)

    # Use a list comprehension to get the IDs of the recommended fields
    recommended_field_ids = [field.pk for field in recommended_fields]

    print("recommended_field_ids: ", recommended_field_ids)

    # Filter out the recommended fields from the field_items queryset
    field_items = field_items.exclude(pk__in=recommended_field_ids)

    try:
        user_skills = UserSkill.objects.filter(user=request.user)
        # user_skills_list = [skill.skill.skill for skill in user_skills]
        highest_skill_level = user_skills.order_by('-level').first()
        # filter top 15 skills
        user_skills = user_skills.order_by('-level')[:15]
        # get multiplier for highest_skill_level that will not exceed 100
        level_multiplier = 100 / highest_skill_level.level
    except:
        user_skills = None
        level_multiplier = 1

    return render(request, 'home.html', {
        'specialization_items': specialization_items, 
        'field_items': recommended_fields + list(field_items),
        'user_recommendations': user_recommendations,
        'user_skills': user_skills,
        'level_multiplier': level_multiplier
        })


#@allowed_users(allowed_roles=['admin','staff','student','instructor'])
def home_field(request, field_id=None):
    print("On home_field, field_id: ", field_id)
    field_items = Field.objects.all()
    selected_field = None

    # Fetch user recommendations
    user_recommendations = None
    recommended_fields = []
    if request.user.is_authenticated:
        user_recommendations = UserRecommendations.objects.filter(user=request.user).first()

    # Create a list to store the recommended fields
    recommended_fields = []

    # Order recommended fields first
    if user_recommendations:
        recommended_fields.extend([user_recommendations.field_1, user_recommendations.field_2, user_recommendations.field_3])

    print("recommended_fields: ", recommended_fields)

    # Use a list comprehension to get the IDs of the recommended fields
    recommended_field_ids = [field.pk for field in recommended_fields]

    print("recommended_field_ids: ", recommended_field_ids)

    # Filter out the recommended fields from the field_items queryset
    field_items = field_items.exclude(pk__in=recommended_field_ids)

    if field_id is not None:
        selected_field = get_object_or_404(Field, field=field_id)
        specialization_items = Specialization.objects.filter(field=selected_field)
        #messages.success(request, "specialization items is filtered")
    else:
        specialization_items = Specialization.objects.all()
        messages.success(request, "specialization items is not filtered")

    #specialization_items = Specialization.objects.all()
    

    return render(request, 'specialization_list.html', {
        'specialization_items': specialization_items,
        'field_items': recommended_fields + list(field_items),
        'selected_field': selected_field,
        'user_recommendations': user_recommendations  # Pass the user recommendations to the template
    })


def status_counts():
    JobPosting_count = JobPosting.objects.all().count()
    Specialization_count = Specialization.objects.all().count()
    QuestionSet_count = QuestionSet.objects.all().count()
    Student_count = User.objects.all().count()
    Survey_count = Survey.objects.all().count()
    return JobPosting_count, Specialization_count, QuestionSet_count, Student_count, Survey_count

#@admin_only # only admin can access this page # if admin only, then no need to add @login_required it will be redundant
def admin_home(request):
    admin = True

    # Get a list of fields
    fields = Field.objects.all()

    # Query to count tests for each field
    field_test_counts = Test.objects.values('field').annotate(test_count=Count('field'))

    # Create a dictionary to store the field names and their corresponding test counts
    field_test_count_dict = {}
    for field_data in field_test_counts:
        field_id = field_data['field']
        test_count = field_data['test_count']
        field_name = Field.objects.get(field=field_id).field_name  # Get the field name
        field_test_count_dict[field_name] = test_count

    courses = Course.objects.all()

    # Get other counts
    auth_user = User.objects.all()
    # JobPosting_count = JobPosting.objects.all().count()
    # Specialization_count = Specialization.objects.all().count()
    # QuestionSet_count = QuestionSet.objects.all().count()
    # Student_count = User.objects.all().count()
    # Survey_count = Survey.objects.all().count()
    LearningMaterial_count = LearningMaterial.objects.all().count()
    JobPosting_count, Specialization_count, QuestionSet_count, Student_count, Survey_count = status_counts()
    return render(request, 'dashboard/admin_home.html', {
        'admin': admin,
        'field_test_count_dict': field_test_count_dict,
        'auth_user': auth_user,
        'courses': courses,
        'LearningMaterial_count': LearningMaterial_count,
        'JobPosting_count': JobPosting_count,
        'Specialization_count': Specialization_count,
        'QuestionSet_count': QuestionSet_count,
        'Student_count': Student_count,
        'Survey_count': Survey_count,
        'fields': fields,  # Pass the list of fields
    })
    

# def admin_course(request, course_id=None, term=None):
#     JobPosting_count, Specialization_count, QuestionSet_count, Student_count, Survey_count = status_counts()
#     course_list = Course.objects.all()
#     current_course = None

#     if course_id is None:
#         # Get a list of courses
#         courses = Course.objects.all()
#         course_name = "All Courses"
#         return render(request, 'dashboard/admin_course.html', {
#             'courses': courses,
#             'course_name': course_name,
#             'QuestionSet_count': QuestionSet_count,
#             'Student_count': Student_count,
#             'Survey_count': Survey_count,
#         })
#     current_course = Course.objects.get(id=course_id)
#     course_term = Course.objects.get(id=course_id).number_of_years
#     # make course_term a list from 1 to course_term
#     course_term_list = list(range(1, course_term+1))


#     if term is None: 
#         course_subjects = User.objects.raw('''
#         SELECT acad_course.*, acad_curriculum.*, acad_subject.*
#         FROM acad_course
#         INNER JOIN acad_curriculum ON acad_course.id = acad_curriculum.course_id
#         INNER JOIN acad_subject ON acad_curriculum.subject_id = acad_subject.id
#         WHERE acad_course.id = %s''', [course_id])
#     else:
#         course_subjects = User.objects.raw('''
#         SELECT acad_course.*, acad_curriculum.*, acad_subject.*
#         FROM acad_course
#         INNER JOIN acad_curriculum ON acad_course.id = acad_curriculum.course_id
#         INNER JOIN acad_subject ON acad_curriculum.subject_id = acad_subject.id
#         WHERE acad_course.id = %s AND acad_curriculum.term = %s''', [course_id, term])
    
#     return render(request, 'dashboard/admin_course.html', {
#         'course_list': course_list, # for dropdown menu
#         'course_subjects': course_subjects,
#         'current_course': current_course,
#         'course_term_list': course_term_list,
#         'QuestionSet_count': QuestionSet_count,
#         'Student_count': Student_count,
#         'Survey_count': Survey_count,
#     })
def admin_course(request):
    JobPosting_count, Specialization_count, QuestionSet_count, Student_count, Survey_count = status_counts()
    course_list = Course.objects.all()
    current_course = None
    current_term = None
    course_id = request.GET.get('course_id')
    term = request.GET.get('term')


    if course_id:
        current_course = Course.objects.get(id=course_id)
        course_term = Course.objects.get(id=course_id).number_of_years
        course_term_list = list(range(1, course_term+1))

        if term:
            if term == 'all':
                current_term = "all"
                course_subjects = User.objects.raw('''
                SELECT acad_course.*, acad_curriculum.*, acad_subject.*
                FROM acad_course
                INNER JOIN acad_curriculum ON acad_course.id = acad_curriculum.course_id
                INNER JOIN acad_subject ON acad_curriculum.subject_id = acad_subject.id
                WHERE acad_course.id = %s''', [course_id])
            else:
                current_term = int(term)
                course_subjects = User.objects.raw('''
                SELECT acad_course.*, acad_curriculum.*, acad_subject.*
                FROM acad_course
                INNER JOIN acad_curriculum ON acad_course.id = acad_curriculum.course_id
                INNER JOIN acad_subject ON acad_curriculum.subject_id = acad_subject.id
                WHERE acad_course.id = %s AND acad_curriculum.year = %s''', [course_id, term])
        else:
            course_subjects = User.objects.raw('''
            SELECT acad_course.*, acad_curriculum.*, acad_subject.*
            FROM acad_course
            INNER JOIN acad_curriculum ON acad_course.id = acad_curriculum.course_id
            INNER JOIN acad_subject ON acad_curriculum.subject_id = acad_subject.id
            WHERE acad_course.id = %s''', [course_id])
    else:
        course_subjects = None
        course_term_list = None

    return render(request, 'dashboard/admin_course.html', {
        'course_list': course_list, # for dropdown menu
        'course_subjects': course_subjects,
        'current_course': current_course,
        'current_term': current_term,
        'course_term_list': course_term_list,
        'QuestionSet_count': QuestionSet_count,
        'Student_count': Student_count,
        'Survey_count': Survey_count,
    })
# def admin_course(request):
#     JobPosting_count, Specialization_count, QuestionSet_count, Student_count, Survey_count = status_counts()
#     course_list = Course.objects.all()
#     current_course = None
#     course_id = request.GET.get('course_id')
#     term = request.GET.get('term')

#     if course_id:
#         current_course = Course.objects.get(id=course_id)
#         course_term = Course.objects.get(id=course_id).number_of_years
#         course_term_list = list(range(1, course_term+1))

#         # if term:
#         #     if term == 'all':
#         #         current_term = "all"
#         #         course_subjects = User.objects.raw('''
#         #         SELECT acad_course.*, acad_curriculum.*, acad_subject.*
#         #         FROM acad_course
#         #         INNER JOIN acad_curriculum ON acad_course.id = acad_curriculum.course_id
#         #         INNER JOIN acad_subject ON acad_curriculum.subject_id = acad_subject.id
#         #         WHERE acad_course.id = %s''', [course_id])
#         #     else:     
#         #         current_term = int(term)
#         #         course_subjects = User.objects.raw('''
#         #         SELECT acad_course.*, acad_curriculum.*, acad_subject.*
#         #         FROM acad_course
#         #         INNER JOIN acad_curriculum ON acad_course.id = acad_curriculum.course_id
#         #         INNER JOIN acad_subject ON acad_curriculum.subject_id = acad_subject.id
#         #         WHERE acad_course.id = %s AND acad_curriculum.year = %s''', [course_id, term])
#         # else:
#         #     current_term = None
#         #     course_subjects = User.objects.raw('''
#         #     SELECT acad_course.*, acad_curriculum.*, acad_subject.*
#         #     FROM acad_course
#         #     INNER JOIN acad_curriculum ON acad_course.id = acad_curriculum.course_id
#         #     INNER JOIN acad_subject ON acad_curriculum.subject_id = acad_subject.id
#         #     WHERE acad_course.id = %s''', [course_id])
#         if term:
#             if term == 'all':
#                 current_term = "all"
#                 course_subjects = Subject.objects.raw('''
#                 SELECT acad_subject.id, acad_subject.subject_name, GROUP_CONCAT(website_skill.skill) as skills
#                 FROM acad_course
#                 INNER JOIN acad_curriculum ON acad_course.id = acad_curriculum.course_id
#                 INNER JOIN acad_subject ON acad_curriculum.subject_id = acad_subject.id
#                 LEFT JOIN acad_subject_skills ON acad_subject.id = acad_subject_skills.subject_id
#                 LEFT JOIN website_skill ON acad_subject_skills.skill_id = website_skill.id
#                 WHERE acad_course.id = %s
#                 GROUP BY acad_subject.id''', [course_id])
#             else:     
#                 current_term = int(term)
#                 # course_subjects = User.objects.raw('''
#                 # SELECT acad_course.*, acad_curriculum.*, acad_subject.*, GROUP_CONCAT(website_skill.skill) as skills
#                 # FROM acad_course
#                 # INNER JOIN acad_curriculum ON acad_course.id = acad_curriculum.course_id
#                 # INNER JOIN acad_subject ON acad_curriculum.subject_id = acad_subject.id
#                 # LEFT JOIN acad_subject_skills ON acad_subject.id = acad_subject_skills.subject_id
#                 # LEFT JOIN website_skill ON acad_subject_skills.skill_id = website_skill.id
#                 # WHERE acad_course.id = %s AND acad_curriculum.year = %s
#                 # GROUP BY acad_subject.id''', [course_id, term])
#                 course_subjects = Subject.objects.raw('''
#                 SELECT acad_subject.id, acad_subject.subject_name, GROUP_CONCAT(website_skill.skill) as skills
#                 FROM acad_course
#                 INNER JOIN acad_curriculum ON acad_course.id = acad_curriculum.course_id
#                 INNER JOIN acad_subject ON acad_curriculum.subject_id = acad_subject.id
#                 LEFT JOIN acad_subject_skills ON acad_subject.id = acad_subject_skills.subject_id
#                 LEFT JOIN website_skill ON acad_subject_skills.skill_id = website_skill.id
#                 WHERE acad_course.id = %s AND acad_curriculum.year = %s
#                 GROUP BY acad_subject.id, acad_subject.name''', [course_id, term])
#         else:
#             current_term = None
#             course_subjects = Subject.objects.raw('''
#             SELECT acad_subject.id, acad_subject.subject_name, GROUP_CONCAT(website_skill.skill) as skills
#             FROM acad_course
#             INNER JOIN acad_curriculum ON acad_course.id = acad_curriculum.course_id
#             INNER JOIN acad_subject ON acad_curriculum.subject_id = acad_subject.id
#             LEFT JOIN acad_subject_skills ON acad_subject.id = acad_subject_skills.subject_id
#             LEFT JOIN website_skill ON acad_subject_skills.skill_id = website_skill.id
#             WHERE acad_course.id = %s
#             GROUP BY acad_subject.id''', [course_id])
#     else:
#         course_subjects = None
#         course_term_list = None
#     # for subject in course_subjects:
#     #     subject.skills = subject.skills.split(',')
#     course_subjects_list = []
#     for subject in course_subjects:
#         subject_dict = {
#             'id': subject.id,
#             'subject_name': subject.subject_name,
#             'skills': subject.skills.split(',') if subject.skills else []
#         }
#         course_subjects_list.append(subject_dict)
#     # if course_subjects:  # make sure the RawQuerySet is not empty
#     #     first_subject = course_subjects[0]
#     #     column_names = [field.name for field in first_subject._meta.fields]
#     #     print(column_names)

#     print("current_course: ", current_course)
#     print("current_term: ", current_term)
#     return render(request, 'dashboard/admin_course.html', {
#         'course_list': course_list, # for dropdown menu
#         'course_subjects': course_subjects_list,
#         'current_course': current_course,
#         'current_term': current_term,
#         'course_term_list': course_term_list,
#         'QuestionSet_count': QuestionSet_count,
#         'Student_count': Student_count,
#         'Survey_count': Survey_count,
#     })

#@admin_only # only admin can access this page # if admin only, then no need to add @login_required it will be redundant
def admin_students(request):
    JobPosting_count, Specialization_count, QuestionSet_count, Student_count, Survey_count = status_counts()
    
    # join by user_id and id
    students = User.objects.raw('''
    SELECT auth_user.*, acad_studentprofile.*, acad_course.course_name as course_name 
    FROM auth_user 
    INNER JOIN acad_studentprofile ON auth_user.id = acad_studentprofile.user_id
    INNER JOIN acad_course ON acad_studentprofile.enrolled_courses_id = acad_course.id
    ''')

    # print firs students all fields
    #print("students: ", students[0].__dict__)
    
    return render(request, 'dashboard/admin_students.html', {
        'students': students,
        'QuestionSet_count': QuestionSet_count,
        'Student_count': Student_count,
        'Survey_count': Survey_count,
        })

def admin_test(request):
    JobPosting_count, Specialization_count, QuestionSet_count, Student_count, Survey_count = status_counts()
    
    questionset = QuestionSet.objects.all()
    # auth_user and questionset join by user_id and id
    questionset = User.objects.raw('''
    SELECT auth_user.*, assessment_questionset.*
    FROM auth_user
    INNER JOIN assessment_questionset ON auth_user.id = assessment_questionset.user_id
    ''')
    

    # disply field names
    print("questionset: ", questionset[0].__dict__)
    
    return render(request, 'dashboard/admin_test.html', {
        'questionset': questionset,
        'QuestionSet_count': QuestionSet_count,
        'Student_count': Student_count,
        'Survey_count': Survey_count,
        })

def admin_tracer(request):
    JobPosting_count, Specialization_count, QuestionSet_count, Student_count, Survey_count = status_counts()
    survey = Survey.objects.all()


    return render(request, 'dashboard/admin_tracer.html', {
        'survey': survey, 
        'QuestionSet_count': QuestionSet_count,
        'Student_count': Student_count,
        'Survey_count': Survey_count,
        })

def admin_jobpostings(request):
    JobPosting_count, Specialization_count, QuestionSet_count, Student_count, Survey_count = status_counts()
    jobpostings = JobPosting.objects.all()
    return render(request, 'dashboard/admin_jobpostings.html', {
        'jobpostings': jobpostings, 
        'QuestionSet_count': QuestionSet_count,
        'Student_count': Student_count,
        'Survey_count': Survey_count,
        })


def admin_LM(request):
    JobPosting_count, Specialization_count, QuestionSet_count, Student_count, Survey_count = status_counts()
    learningmaterial = LearningMaterial.objects.all()
    return render(request, 'dashboard/admin_LM.html', {
        'learningmaterial': learningmaterial, 
        'QuestionSet_count': QuestionSet_count,
        'Student_count': Student_count,
        'Survey_count': Survey_count,
        })


@unauthenticated_user # instead of adding if user.is_authenticated, use this decorator
def login_user(request):
    if request.method == 'POST':
        #email = request.POST['email']
        username=request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('paths')
        else:
            messages.success(request, 'Error logging in')
            return redirect('login_user')
    else:
        return render(request, 'user/login.html')

@unauthenticated_user
def sign_in(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')            
            user = authenticate(username=username, password=password)
            # check if student group exisits
            # else create group
            #group = Group.objects.get(name='student')
            #user.groups.add(group)
            login(request,user)
            messages.success(request, 'Student ' + username + ' have successfully created an account')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'user/sign_in.html', {'form': form})
    
    # After successfully registering the user, trigger the signal
    # user = get_user_model().objects.get(username=new_user_username)
    # user_registered.send(sender=user)


    return render(request, 'user/sign_in.html', {'form': form})


def forgot_password(request):
    return render(request, 'user/forgot_password.html')


def recovery(request):
    return render(request, 'user/recovery.html')

def landing_page(request):
    return render(request, 'landing.html')

def paths(request):
    return render(request,'test/paths.html' )



#########################################################################
# ------------------------for user module------------------------------ #
#########################################################################

@login_required  # Ensure that the user is logged in to access the profile
def user_profile(request):
    user = request.user
    # Query additional user profile data if using a custom user profile model
    context = {'user': user}
    return render(request, 'user/user_profile.html', context)

@login_required(login_url='login_user')
def edit_profile(request):
    
    user = request.user
    print(user.username,user.first_name,user.last_name,user.email)
    if request.method == 'POST':
        # Retrieve form inputs
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')

        # Update the user's profile
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        return redirect('user_profile')
    
    return render(request, 'user/edit_profile.html')

@login_required(login_url='login_user')
def terms_and_conditions(request):
    user = request.user
    # Query additional user profile data if using a custom user profile model
    context = {'user': user}
    return render(request, 'user/terms_and_conditions.html', context)

@login_required(login_url='login_user')
def settings(request):
    user = request.user
    if request.method == 'POST':
        
        new_password1 = request.POST.get('new_password')
        new_password2 = request.POST.get('confirm_password')


        # Check if new passwords match
        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match. Please try again.')
            return redirect('change_password')

        # Update the user's password
        request.user.set_password(new_password1)
        request.user.save()

        # Update the user's session to avoid logging out after a password change
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Your password was successfully updated!')
        return redirect('user_profile')
    
    return render(request, 'user/settings.html')

class CustomLogoutView(LogoutView):
    template_name = 'user/custom_logout.html'  # Optionally, specify a custom logout template

    def get_next_page(self):
        # Customize the redirection logic if needed
        next_page = super().get_next_page()
        # You can add additional logic here if required
        return next_page

#########################################################################
# -----------------------for specialization---------------------------- #
#########################################################################


def specialization_page(request, item_id):
    # Retrieve the selected specialization item or return a 404 error if it doesn't exist
    specialization_item = get_object_or_404(Specialization, pk=item_id)

    # Render the specialization_page template with the item
    return render(request, 'specialization_page.html', {'specialization_item': specialization_item})



def field_page(request, field_id=None):

    # Field object
    field_object = Field.objects.get(field=field_id)

    # get specialization items with field_id
    specialization_items = Specialization.objects.filter(field=field_id)

    #print("Field page,  SPecialization items: ", specialization_items)

    # Get Test objects with field_id
    test_items = Test.objects.filter(field=field_id)
    
    return render(request, 'field.html', {'field_object' : field_object, 'specialization_items': specialization_items, 'test_items': test_items})



###########################################Engr Umair Worked ##################################
def upload_profile_pic(request):
    if request.method == "POST":
        profile_picture = request.FILES.get('profile_picture')
        obj = UserProfile(user=request.user,profile_picture=profile_picture)
        obj.save()
        return redirect("user_profile")
    return render(request,"user/upload.html")
def remove_profile_picture(request):
    obj = UserProfile.objects.get(user=request.user)
    
    obj.delete()
    return redirect("user_profile")
def reports(request,id):
    surveys = Survey.objects.filter(user=id)
    s_count = surveys.count()
    context = {'surveys': surveys,'s_count' : s_count} 
    return render(request, 'reports.html', context)
    