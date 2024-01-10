
from django.urls import path, include
from apps.website import views
from django.contrib.auth.views import LogoutView

# import datetime and timezone
from datetime import datetime
from django.utils import timezone

urlpatterns = [
    path('home', views.home, name='home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('field/', views.home_field, name='home_field'),
    path('field/<int:field_id>/', views.home_field, name='home_field'),

    # For Authentication
    path('login_user/', views.login_user, name='login_user'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('recovery/', views.recovery, name='recovery'),
    path('send-test-email/', views.send_test_email, name='send_test_email'),
    path('verify_email/<int:id>/', views.verify_email, name='verify_email'),
    # For User Page
    path('profile/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('settings/', views.settings, name='settings'),
    
    # Logout
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('logout/success/', LogoutView.as_view(template_name='user/logout_success.html'), name='logout_success'),
    
    # For Field
    path('field_page/<int:field_id>/', views.field_page, name='field_page'),

    # For Specialization
    path('specialization_page/<int:item_id>/', views.specialization_page, name='specialization_page'),

    #for landing page
    path('', views.landing_page, name='landing_page'),
    path('paths/', views.paths, name = 'paths'),

    # for admin dashboard
    path('admin_course/', views.admin_course, name='admin_course'),
    path('admin_course/<int:course_id>/', views.admin_course, name='admin_course'),
    path('admin_course/<int:course_id>/<int:term>/', views.admin_course, name='admin_course'),
    path('admin_students',views.admin_students, name='admin_students'),
    path('admin_end_term/', views.admin_end_term, name='admin_end_term'),
    path('admin_test', views.admin_test, name='admin_test'),
    path('admin_tracer', views.admin_tracer, name='admin_tracer'),
    path('admin_jobpostings', views.admin_jobpostings, name='admin_jobpostings'),
    path('admin_LM', views.admin_LM, name='admin_LM'),

    # path('admin_report/', views.admin_report, name='admin_report'),
    # path('admin_report_view/', views.admin_report_view, name='admin_report_view'),
    # path('admin_report_pdf/', views.admin_report_pdf, name='admin_report_pdf'),
    # path("reports/<int:id>/", views.reports, name="reports"),
    
    
    #for grade levl
    # path ('', views.grade_level, name='grade_level'),


   #########################################Work By Engr Umair####################################
   path("upload_profile_pic/",views.upload_profile_pic, name="uploadprofilepic"),
   path("remove_profile_picture/", views.remove_profile_picture, name="removeprofilepicture"),

]


