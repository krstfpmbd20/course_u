from django.shortcuts import render, redirect
from .forms import SurveyForm
from django.http import HttpResponse

from django.http import FileResponse
import datetime
from .dump.report_generator import *
from .dump.plotgenerator import *
from xhtml2pdf import pisa
from django.template.loader import get_template


def survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('thank_you')
    else:
        form = SurveyForm()

    return render(request, 'survey/survey.html', {'form': form})

def thank_you(request):
    return render(request, 'survey/thank_you.html')




def admin_report(request):
    # get current time
    current_time = datetime.datetime.now()
    
    # get first and last as name
    first_name = request.user.first_name
    last_name = request.user.last_name
    name = first_name + " " + last_name
    if first_name == "" and last_name == "":
        name = request.user.username
    

    # Generate all necessary plots
    alignment_and_satisfaction = generate_alignment_and_satisfaction()
    role_satisfaction_by_academic_specialization = generate_role_satisfaction_by_academic_specialization()
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

    return render(request, 'dashboard/admin_report.html', {
        'current_time': current_time,
        'name': name,
        'alignment_and_satisfaction': alignment_and_satisfaction,
        'role_satisfaction_by_academic_specialization': role_satisfaction_by_academic_specialization,
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


def admin_report_view(request):
     # get current time
    current_time = datetime.datetime.now()
    
    # get first and last as name
    first_name = request.user.first_name
    last_name = request.user.last_name
    name = first_name + " " + last_name
    if first_name == "" and last_name == "":
        name = request.user.username

    # Generate all necessary plots
    alignment_and_satisfaction = plotly_alignment_and_satisfaction()
    alignment_and_satisfaction2 = chart_alignment_and_satisfaction()

    return render(request, 'dashboard/admin_report_view.html', {
        'current_time': current_time,
        'name': name,
        'alignment_and_satisfaction': alignment_and_satisfaction,
        'alignment_and_satisfaction2': alignment_and_satisfaction2,
        #'role_satisfaction_by_academic_specialization': role_satisfaction_by_academic_specialization,
    })


def admin_report_pdf(request):
    # get current time
    current_time = datetime.datetime.now()
    
    # get first and last as name
    first_name = request.user.first_name
    last_name = request.user.last_name
    name = first_name + " " + last_name
    if first_name == "" and last_name == "":
        name = request.user.username
    # image_path = os.path.join(settings.STATICFILES_DIRS[0], 'images/report-logo.png')
    # #image_path = staticfiles_storage.path(static('images/report-logo.png'))
    # with open(image_path, 'rb') as image_file:
    #     base64_logo = base64.b64encode(image_file.read()).decode('utf-8')

     # Generate all necessary plots
    alignment_and_satisfaction = generate_alignment_and_satisfaction()
    role_satisfaction_by_academic_specialization = generate_role_satisfaction_by_academic_specialization()
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
    template = get_template('dashboard/admin_report.html')
    context = {
        'current_time': current_time,
        'name': name,
        # 'base64_logo': base64_logo,
        'alignment_and_satisfaction': alignment_and_satisfaction,
        'role_satisfaction_by_academic_specialization': role_satisfaction_by_academic_specialization,
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
    }
    html = template.render(context)

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create a PDF file
    pisa_status = pisa.CreatePDF(html, dest=buffer)

    # If error, show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    buffer.seek(0)

    # Make a pdf response
    pdf = FileResponse(buffer, filename='admin_report.pdf')
    pdf['Content-Disposition'] = 'attachment; filename="admin_report.pdf"'
    return pdf
