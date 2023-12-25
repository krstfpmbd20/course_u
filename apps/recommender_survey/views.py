from django.shortcuts import render, redirect
from .models import Survey
from .forms import SurveyForm
from apps.recommender.models import UserRecommendations

from apps.acad.models import StudentProfile

def survey(request):
    prev_year = StudentProfile.objects.filter(user=request.user).first().current_year - 1
    # get recommendation from previous year where user = request.user and year = prev_year
    last_recommendation = UserRecommendations.objects.filter(user_id=request.user, current_year=prev_year).last()

    # check if reco survey exists where recommendation_id = last_recommendation.recommendation_id
    reco_survey = Survey.objects.filter(recommendation_id=last_recommendation.recommendation_id).first()
    if reco_survey:
        # if reco survey exists, redirect to recommender
        return redirect('recommender')


    # If there's a recommendation and no answered survey, go to survey
    survey = Survey.objects.filter(recommendation_id=last_recommendation.recommendation_id).first()
    if not survey:
        if request.method == 'POST':
            form = SurveyForm(request.POST)
            if form.is_valid():
                # Save userrecommendation_id to recommender survey
                survey = form.save(commit=False)
                survey.recommendation_id = last_recommendation.recommendation_id
                survey.save()
                return redirect('recommender_thank_you')
        else:
            form = SurveyForm()

        return render(request, 'recommendersurvey/survey.html', {'form': form})

    # If there's a recommendation and have answered survey, go to recommendedr
    else:
        return redirect('recommender')

def thank_you(request):
    return render(request, 'recommendersurvey/thank_you.html')