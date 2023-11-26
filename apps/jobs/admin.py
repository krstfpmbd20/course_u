from django.contrib import admin
from apps.jobs.models import JobPosting
from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
from django.http import HttpResponse

from django.urls import path
from  django.urls import reverse

import csv


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()
    

class JobPostingAdmin(admin.ModelAdmin):
    #list_display = ['field', 'field_name','description']  # Customize as needed
    #search_fields = ['field_name']  # Customize as needed

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.upload_csv),
        ]
        return custom_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'File is not CSV type')
                return redirect("/admin/jobs/jobposting/")

            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                created = JobPosting.objects.update_or_create(
                    id=row['id'],
                    link=row['link'],
                    keyword=row['keyword'],
                    job_title=row['job_title'],
                    company_name=row['company_name'],
                    company_link=row['company_link'],
                    date_posted=row['date_posted'],
                    location=row['location'],
                    employment_type=row['employment_type'],
                    job_function=row['job_function'],
                    industries=row['industries'],
                    seniority_level=row['seniority_level'],
                    job_description=row['job_description'],
                    field_id=row['field_id'],
                )
            url = reverse('admin:jobs_jobposting_changelist')
            messages.success(request, 'Your csv file has been imported')
            return redirect(url)

        form = CsvImportForm()
        data = {"form": form, }

        return render (request, "admin/upload_csv.html", data)


# Register your models here.
admin.site.register(JobPosting, JobPostingAdmin)