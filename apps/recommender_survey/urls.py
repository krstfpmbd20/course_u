from django.urls import path
from apps.recommender_survey.views import survey, thank_you, survey_validation

urlpatterns = [
    path('recommender_survey_validation/', survey_validation, name='recommender_survey_validation'),
    path('recommendersurvey/', survey, name='recommender_survey'),
    path('recommender_thank_you/', thank_you, name='recommender_thank_you'),
]
