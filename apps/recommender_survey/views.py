from django.shortcuts import render, redirect
from .models import Survey
from .forms import SurveyForm
from apps.recommender.models import UserRecommendations

from apps.acad.models import StudentProfile

def survey(request):
    try:
        prev_year = StudentProfile.objects.filter(user=request.user).first().current_year - 1
    except:
        # direct to test home
        prev_year = False
    
    if prev_year == False:
        return redirect('test_home')
    
    # get recommendation from previous year where user = request.user and year = prev_year
    
    try:
        last_recommendation = UserRecommendations.objects.filter(user_id=request.user, current_year=prev_year).last()
    except:
        last_recommendation = None
    if  last_recommendation == None:
        return redirect('recommender')

    # check if reco survey exists where recommendation_id = last_recommendation.recommendation_id
    try:
        reco_survey = Survey.objects.filter(recommendation_id=last_recommendation.recommendation_id).first()
    except:
        reco_survey = None
    if reco_survey == None:
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