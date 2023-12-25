from django.urls import path
from apps.survey import views

urlpatterns = [
    path('survey/', views.survey, name='survey'),
    path('thank_you/', views.thank_you, name='thank_you'),

    path('admin_report/', views.admin_report, name='admin_report'),
    path('admin_report_view/', views.admin_report_view, name='admin_report_view'),
    path('admin_report_pdf/', views.admin_report_pdf, name='admin_report_pdf'),
    # path("reports/<int:id>/", views.reports, name="reports"),
    
    

]
