from django.shortcuts import render, redirect
from .forms import SurveyForm
from django.http import HttpResponse

from django.http import FileResponse
import datetime
# from .dump.report_generator import *
# from .dump.plotgenerator import *
from .tracer_report import *

# from xhtml2pdf import pisa
from django.template.loader import get_template

from django.template.loader import render_to_string
# from weasyprint import HTML
# import vharfbuzz
# from reportlab.pdfgen import canvas
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
# from reportlab.lib.styles import getSampleStyleSheet
# from html5lib import parse  # If using html5lib for parsing
# from reportlab.lib import colors
# from io import BytesIO


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
    


    return render(request, 'dashboard/admin_report.html', {
        'current_time': current_time,
        'name': name,

        # PLOTS
        # Recommendation Impact
        'confidence_rating':  to_img(fig_confidence_rating(tracer_dataframe())),
        'recommendation_influence': to_img(fig_recommendation_influence(tracer_dataframe())),
        # word cloud
        
        # Job Alignment and Satisfaction
        'alignment_and_satisfaction': to_img(fig_alignment_and_satisfaction(tracer_dataframe())),
        'job_alignment': to_img(fig_job_alignment(tracer_dataframe())),
        # 'job_alignment_bubble': html_fig_job_alignment_bubble(tracer_dataframe()),
        
        # Time-Series Analysis  
        # bar
        'job_alignment_across_cohorts': to_img(fig_job_alignment_across_cohorts(tracer_dataframe())),
        'job_alignment_time_series' : to_img(fig_job_alignment_time_series(tracer_dataframe())),
        # line
        # over_year
        'confidence_rating_time_series' : to_img(fig_confidence_rating_time_series(tracer_dataframe())),
        
        
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

    return render(request, 'dashboard/admin_report_view.html', {
        'current_time': current_time,
        'name': name,
        
        # PLOTS
        # Recommendation Impact
        'confidence_rating':  html_fig_confidence_rating(tracer_dataframe()),
        'tbl_confidence_rating': table_confidence_rating(tracer_dataframe()),
        'recommendation_influence': html_fig_recommendation_influence(tracer_dataframe()),
        'tbl_recommendation_influence': table_recommendation_influence(tracer_dataframe()),
        # word cloud
        'remakrs_recommendation_influence': remakrs_recommendation_influence(tracer_dataframe()),
        
        # Job Alignment and Satisfaction
        'alignment_and_satisfaction': html_fig_alignment_and_satisfaction(tracer_dataframe()),
        'job_alignment': html_fig_job_alignment(tracer_dataframe()),
        'tbl_job_alignment': table_job_alignment(tracer_dataframe()),
        # 'job_alignment_bubble': html_fig_job_alignment_bubble(tracer_dataframe()),
        
        # Time-Series Analysis  
        # bar
        # 'job_alignment_across_cohorts': html_fig_job_alignment_across_cohorts(tracer_dataframe()),
        # 'job_alignment_time_series' : html_fig_job_alignment_time_series(tracer_dataframe()),
        # line
        # over_year
        # 'confidence_rating_time_series' : html_fig_confidence_rating_time_series(tracer_dataframe()),
        'remarks_additional_feedback': remarks_additional_feedback(tracer_dataframe()),
    })

def admin_report_pdf(request):
    # create blank pdf file
    # pdf = FPDF()
    # pdf.add_page()
    # pdf = pdf.output('admin_report.pdf', 'F')
    return None
# def admin_report_pdf(request):
#     # get current time
#     current_time = datetime.datetime.now()
    
#     # get first and last as name
#     first_name = request.user.first_name
#     last_name = request.user.last_name
#     name = first_name + " " + last_name
#     if first_name == "" and last_name == "":
#         name = request.user.username
#     # image_path = os.path.join(settings.STATICFILES_DIRS[0], 'images/report-logo.png')
#     # #image_path = staticfiles_storage.path(static('images/report-logo.png'))
#     # with open(image_path, 'rb') as image_file:
#     #     base64_logo = base64.b64encode(image_file.read()).decode('utf-8')

#      # Generate all necessary plots


#     template = get_template('dashboard/admin_report.html')
#     context = {
#         'current_time': current_time,
#         'name': name,
#         # 'base64_logo': base64_logo,

#         # PLOTS
#         # Recommendation Impact
#         'confidence_rating':  bytes(to_img(fig_confidence_rating(tracer_dataframe()))),
#         'recommendation_influence': to_img(fig_recommendation_influence(tracer_dataframe())),
#         # word cloud
        
#         # Job Alignment and Satisfaction
#         'alignment_and_satisfaction': to_img(fig_alignment_and_satisfaction(tracer_dataframe())),
#         'job_alignment': to_img(fig_job_alignment(tracer_dataframe())),
#         # 'job_alignment_bubble': html_fig_job_alignment_bubble(tracer_dataframe()),
        
#         # Time-Series Analysis  
#         # bar
#         'job_alignment_across_cohorts': to_img(fig_job_alignment_across_cohorts(tracer_dataframe())),
#         'job_alignment_time_series' : to_img(fig_job_alignment_time_series(tracer_dataframe())),
#         # line
#         # over_year
#         'confidence_rating_time_series' : to_img(fig_confidence_rating_time_series(tracer_dataframe())),
        
        
        
#     }
#     html = template.render(context)

#     # # Create a file-like buffer to receive PDF data
#     # buffer = BytesIO()

#     # # Create a PDF file
#     # pisa_status = pisa.CreatePDF(html, dest=buffer)

#     # # # If error, show some funy view
#     # if pisa_status.err:
#     #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     # buffer.seek(0)

#     # Make a pdf response
#     #pdf = FileResponse(buffer, filename='admin_report.pdf')
#     #pdf['Content-Disposition'] = 'attachment; filename="admin_report.pdf"'
#     #return pdf

#     # # Render your HTML template with context
#     # html_string = render_to_string('dashboard/admin_report.html', context=context)

#     # # Create a WeasyPrint HTML object
#     # html = HTML(string=html_string)

#     # # Generate the PDF content
#     # pdf_data = html.write_pdf()

#     # # Create a response with PDF content and appropriate headers
#     # response = HttpResponse(pdf_data, content_type='application/pdf')
#     # response['Content-Disposition'] = 'attachment; filename="admin_report.pdf"'
    
#     #pdf = canvas.Canvas("admin_report.pdf")
#     doc = SimpleDocTemplate("admin_report.pdf")

#     # Parse HTML (if using html5lib)
#     if using_html5lib:
#         parsed_html = parse(html)
#         # Create Platypus elements from parsed HTML structure
#     else:

#     return response



# def admin_report_pdf(request):
#     # get current time
#     current_time = datetime.datetime.now()
    
#     # get first and last as name
#     first_name = request.user.first_name
#     last_name = request.user.last_name
#     name = first_name + " " + last_name
#     if first_name == "" and last_name == "":
#         name = request.user.username
#     # image_path = os.path.join(settings.STATICFILES_DIRS[0], 'images/report-logo.png')
#     # #image_path = staticfiles_storage.path(static('images/report-logo.png'))
#     # with open(image_path, 'rb') as image_file:
#     #     base64_logo = base64.b64encode(image_file.read()).decode('utf-8')

#      # Generate all necessary plots

#     template = get_template('dashboard/admin_report.html')
#     context = {
#         'current_time': current_time,
#         'name': name,
#         # 'base64_logo': base64_logo,

#         # PLOTS
#         # Recommendation Impact
#         'confidence_rating':  bytes(to_img(fig_confidence_rating(tracer_dataframe()))),
#         'recommendation_influence': to_img(fig_recommendation_influence(tracer_dataframe())),
#         # word cloud
        
#         # Job Alignment and Satisfaction
#         'alignment_and_satisfaction': to_img(fig_alignment_and_satisfaction(tracer_dataframe())),
#         'job_alignment': to_img(fig_job_alignment(tracer_dataframe())),
#         # 'job_alignment_bubble': html_fig_job_alignment_bubble(tracer_dataframe()),
        
#         # Time-Series Analysis  
#         # bar
#         'job_alignment_across_cohorts': to_img(fig_job_alignment_across_cohorts(tracer_dataframe())),
#         'job_alignment_time_series' : to_img(fig_job_alignment_time_series(tracer_dataframe())),
#         # line
#         # over_year
#         'confidence_rating_time_series' : to_img(fig_confidence_rating_time_series(tracer_dataframe())),
        
        
#     }
#     html = template.render(context)

#     # Parse HTML (if using html5lib)
#     if using_html5lib:
#         parsed_html = parse(html)
#         # Create Platypus elements from parsed HTML structure
#     else:
#         parsed_html = None

#     return parsed_html


# def admin_report_pdf(request):
#     # get current time
#     current_time = datetime.datetime.now()
    
#     # get first and last as name
#     first_name = request.user.first_name
#     last_name = request.user.last_name
#     name = first_name + " " + last_name
#     if first_name == "" and last_name == "":
#         name = request.user.username
#     # image_path = os.path.join(settings.STATICFILES_DIRS[0], 'images/report-logo.png')
#     # #image_path = staticfiles_storage.path(static('images/report-logo.png'))
#     # with open(image_path, 'rb') as image_file:
#     #     base64_logo = base64.b64encode(image_file.read()).decode('utf-8')

#      # Generate all necessary plots

#     template = get_template('dashboard/admin_report.html')
#     context = {
#         'current_time': current_time,
#         'name': name,
#         # 'base64_logo': base64_logo,

#         # PLOTS
#         # Recommendation Impact
#         'confidence_rating':  bytes(to_img(fig_confidence_rating(tracer_dataframe()))),
#         'recommendation_influence': to_img(fig_recommendation_influence(tracer_dataframe())),
#         # word cloud
        
#         # Job Alignment and Satisfaction
#         'alignment_and_satisfaction': to_img(fig_alignment_and_satisfaction(tracer_dataframe())),
#         'job_alignment': to_img(fig_job_alignment(tracer_dataframe())),
#         # 'job_alignment_bubble': html_fig_job_alignment_bubble(tracer_dataframe()),
        
#         # Time-Series Analysis  
#         # bar
#         'job_alignment_across_cohorts': to_img(fig_job_alignment_across_cohorts(tracer_dataframe())),
#         'job_alignment_time_series' : to_img(fig_job_alignment_time_series(tracer_dataframe())),
#         # line
#         # over_year
#         'confidence_rating_time_series' : to_img(fig_confidence_rating_time_series(tracer_dataframe())),
        
        
#     }
#     html = template.render(context)
#     # Create a PDF document
#     doc = SimpleDocTemplate("admin_report.pdf")
#     styles = getSampleStyleSheet()
#     elements = []

#     # Add text elements
#     elements.append(Paragraph("Report generated for: " + name, styles["Normal"]))
#     #elements.append(Paragraph(str(current_time), styles["Normal"]))
#     #elements.append(Spacer(1, 12))  # Add spacing

#     # # Add plots as images
#     # for plot_name, plot_image in context.items():
#     #     if plot_name.startswith("_"):  # Skip internal variables
#     #         continue
#     #     elements.append(Paragraph(plot_name.replace("_", " ").title(), styles["Heading1"]))
#     #     elements.append(Spacer(1, 6))
#     #     try:
#     #         #elements.append(Image(BytesIO(plot_image), width=400, height=300))  # Adjust dimensions as needed
#     #         elements.append(Paragraph(str(current_time), styles["Normal"]))
#     #     except AttributeError:
#     #         # Handle non-image plot data (e.g., HTML)
#     #         elements.append(Paragraph("Plot not available for display in PDF", styles["Normal"]))
#     #     elements.append(Spacer(1, 12))

#     # Build the PDF
#     doc.build(elements)
#     # print(reportlab.__version__)
#     # Return PDF response
#     pdf_buffer = BytesIO()
#     # doc.save(pdf_buffer)
#     # doc.write(pdf_buffer)

#     doc.build(elements)#, stream=pdf_buffer)  # Use `build` instead of `save`
#     pdf_buffer.seek(0)
#     return FileResponse(pdf_buffer, filename="admin_report.pdf")