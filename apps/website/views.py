from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import LogoutView
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import update_session_auth_hash

#from website.utils import *
from apps.website.forms import SignUpForm, StudentScoreForm
from apps.website.models import Specialization, Field
from apps.recommender.models import UserRecommendations

from apps.assessment.models import Test, QuestionSet
from apps.jobs.models import JobPosting

from utilities.decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
# Other Imports
import json
import logging
import plotly.express as px
from apps.survey.models import Survey
from .plotgenerator import *
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


    return render(request, 'home.html', {
        'specialization_items': specialization_items, 
        'field_items': recommended_fields + list(field_items),
        'user_recommendations': user_recommendations
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

    # Get other counts
    auth_user = User.objects.all()
    JobPosting_count = JobPosting.objects.all().count()
    Specialization_count = Specialization.objects.all().count()
    QuestionSet_count = QuestionSet.objects.all().count()

    return render(request, 'admin_home.html', {
        'admin': admin,
        'field_test_count_dict': field_test_count_dict,
        'auth_user': auth_user,
        'JobPosting_count': JobPosting_count,
        'Specialization_count': Specialization_count,
        'QuestionSet_count': QuestionSet_count,
        'fields': fields,  # Pass the list of fields
    })
    

@admin_only # only admin can access this page # if admin only, then no need to add @login_required it will be redundant
def admin_students(request):
    auth_user = User.objects.all()
    return render(request, 'admin_students.html', {'auth_user': auth_user})


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
            return redirect('home')
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
def extract_relevant_data(survey_responses):
    # Extract relevant fields from survey responses
    extracted_data = []
    for survey_response in survey_responses:
        #student_name = survey_response.student.name
        #job_title = survey_response.job_title
        #satisfaction = survey_response.satisfaction

        #1.	What was your academic specialization in Information Technology or Computer Science during your undergraduate studies?
        course = survey_response.q1     # IT or CS
        #2.	To what extent do you feel that your academic specialization aligns with your current job responsibilities?
        alignment = survey_response.q2  #  Completely Aligned, Mostly Aligned, Somewhat Aligned, Not Aligned at All
        #3.	How well did your academic specialization prepare you for the specific tasks and challenges you face in your current role?
        preparation = survey_response.q3 # very well, well, neutral, poorly, not at all
        #4.	Have you pursued any additional certifications or training after graduation to enhance your skills for your current job?
        additional_sup = survey_response.q4 # 1 (yes) 0 (no)
        #5.	In hindsight, do you think a different academic specialization might have better prepared you for your current career?
        better_preparation = survey_response.q5 # yes no 
        #6.	How satisfied are you with your current job in terms of alignment with your academic specialization and overall career growth?
        satisfaction = survey_response.q6 # # very satisfied, satisfied, neutral, dissatisfied, very dissatisfied

        extracted_data.append({
            #'student_name': student_name,
            #'job_title': job_title,
            #'satisfaction': satisfaction
            'course': course,
            'alignment': alignment,
            'preparation': preparation,
            'additional_sup': additional_sup,
            'better_preparation': better_preparation,
            'satisfaction': satisfaction
        })

    return extracted_data
def analyze_preparation_by_course(extracted_data):
    it_preparation_counts = {}
    cs_preparation_counts = {}
    for data_item in extracted_data:
        course = data_item['course']
        preparation_level = data_item['preparation']

        if course == 'IT':
            if preparation_level not in it_preparation_counts:
                it_preparation_counts[preparation_level] = 0
            it_preparation_counts[preparation_level] += 1

        elif course == 'CS':
            if preparation_level not in cs_preparation_counts:
                cs_preparation_counts[preparation_level] = 0
            cs_preparation_counts[preparation_level] += 1

    preparation_levels_by_course = {
        'IT': it_preparation_counts,
        'CS': cs_preparation_counts
    }

    return preparation_levels_by_course

def calculate_alignment_percentages(extracted_data):
    alignment_counts = {}
    for data_item in extracted_data:
        alignment_level = data_item['alignment']
        if alignment_level not in alignment_counts:
            alignment_counts[alignment_level] = 0
        alignment_counts[alignment_level] += 1

    alignment_percentages = {}
    for alignment_level, count in alignment_counts.items():
        alignment_percentages[alignment_level] = round(count / len(extracted_data) * 100, 2)

    return alignment_percentages
def analyze_additional_certifications(extracted_data):
    additional_certifications_counts = {}
    for data_item in extracted_data:
        additional_certifications = data_item['additional_sup']
        if additional_certifications not in additional_certifications_counts:
            additional_certifications_counts[additional_certifications] = 0
        additional_certifications_counts[additional_certifications] += 1

    additional_certifications_data = {
        'yes': additional_certifications_counts[1],
        'no': additional_certifications_counts[0]
    }

    return additional_certifications_data
def analyze_better_preparation(extracted_data):
    better_preparation_counts = {}
    for data_item in extracted_data:
        better_preparation = data_item['better_preparation']
        if better_preparation not in better_preparation_counts:
            better_preparation_counts[better_preparation] = 0
        better_preparation_counts[better_preparation] += 1

    better_preparation_data = {
        'yes': better_preparation_counts['Yes'],
        'no': better_preparation_counts['No'],
        'not_sure': better_preparation_counts['Not Sure']
    }

    return better_preparation_data

def analyze_overall_satisfaction(extracted_data):
    satisfaction_counts = {}
    for data_item in extracted_data:
        satisfaction_level = data_item['satisfaction']
        if satisfaction_level not in satisfaction_counts:
            satisfaction_counts[satisfaction_level] = 0
        satisfaction_counts[satisfaction_level] += 1

    overall_satisfaction_percentages = {}
    for satisfaction_level, count in satisfaction_counts.items():
        percentage = round(count / len(extracted_data) * 100, 2)
        overall_satisfaction_percentages[satisfaction_level] = percentage

    return overall_satisfaction_percentages
def analyze_data(extracted_data):
    # Perform data analysis
    alignment_percentages = calculate_alignment_percentages(extracted_data)
    preparation_levels_by_course = analyze_preparation_by_course(extracted_data)
    additional_certifications_data = analyze_additional_certifications(extracted_data)
    better_preparation_data = analyze_better_preparation(extracted_data)
    overall_satisfaction_percentages = analyze_overall_satisfaction(extracted_data)

    # Prepare data for HTML template
    alignment_data = {
        'title': 'Alignment with Academic Specialization',
        'labels': alignment_percentages.keys(),
        'data': alignment_percentages.values()
    }

    preparation_data = {
        'title': 'Preparation Levels by Course',
        'courses': ['IT', 'CS'],
        'preparation_levels': ['Very Well', 'Well', 'Neutral', 'Poorly', 'Not at All'],
        'data': preparation_levels_by_course
    }

    additional_certifications = {
        'title': 'Additional Certifications',
        'labels': ['Yes', 'No'],
        'data': additional_certifications_data
    }

    better_preparation = {
        'title': 'Satisfaction with Better Preparation',
        'labels': ['Yes', 'No', 'Not Sure'],
        'data': better_preparation_data
    }

    overall_satisfaction = {
        'title': 'Overall Satisfaction',
        'labels': overall_satisfaction_percentages.keys(),
        'data': overall_satisfaction_percentages.values()
    }

    # Return analyzed data for use in HTML template
    return {
        'alignment_data': alignment_data,
        'preparation_data': preparation_data,
        'additional_certifications': additional_certifications,
        'better_preparation': better_preparation,
        'overall_satisfaction': overall_satisfaction
    }
def process_survey_data(survey_responses):
    # Extract relevant data from survey responses
    # This may involve filtering, aggregating, or transforming data
    extracted_data = extract_relevant_data(survey_responses)

    # Calculate statistics or generate visualizations
    # This may involve using data analysis libraries or charting tools
    processed_data = analyze_data(extracted_data)

    return processed_data



def admin_report(request):
    # Generate all necessary plots
    gender_distribution_plot = generate_gender_distribution_plot()
    civil_status_distribution_plot = generate_civil_status_distribution_plot()
    academic_specialization_distribution_plot = generate_academic_specialization_distribution_plot()
    alignment_with_job_responsibilities_plot = generate_alignment_with_job_responsibilities_plot()
    satisfaction_levels_plot = generate_satisfaction_levels_plot()
    certifications_training_percentage_plot = generate_certifications_training_percentage_plot()
    different_specialization_percentage_plot = generate_different_specialization_percentage_plot()
    overall_satisfaction_plot = generate_overall_satisfaction_plot()
    job_fields_distribution_plot = generate_job_fields_distribution_plot()
    user_engagement_plot = generate_user_engagement_plot()
    return render(request, 'admin_report.html', {
        'gender_distribution_plot': gender_distribution_plot,
        'civil_status_distribution_plot': civil_status_distribution_plot,
        'academic_specialization_distribution_plot': academic_specialization_distribution_plot,
        'alignment_with_job_responsibilities_plot': alignment_with_job_responsibilities_plot,
        'satisfaction_levels_plot': satisfaction_levels_plot,
        'certifications_training_percentage_plot': certifications_training_percentage_plot,
        'different_specialization_percentage_plot': different_specialization_percentage_plot,
        'overall_satisfaction_plot': overall_satisfaction_plot,
        'job_fields_distribution_plot': job_fields_distribution_plot,  
        'user_engagement_plot': user_engagement_plot,
    })
def field_page(request, field_id=None):

    # Field object
    field_object = Field.objects.get(field=field_id)

    # get specialization items with field_id
    specialization_items = Specialization.objects.filter(field=field_id)

    print("Field page,  SPecialization items: ", specialization_items)

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
    