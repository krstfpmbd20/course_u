from django.contrib import admin
from apps.acad.models import Course, Subject, Curriculum, StudentGrades, StudentProfile
from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
from django.http import HttpResponse

from django.urls import path
from  django.urls import reverse

import csv


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()
    


class SubjectAdmin(admin.ModelAdmin):
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
                return redirect("/admin/acad/subject/")

            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                created = Subject.objects.update_or_create(
                    id=row['id'],
                    subject_name=row['subject_name'],
                    description=row['description'],
                )
            url = reverse('admin:acad_subject_changelist')
            messages.success(request, 'Your csv file has been imported')
            return redirect(url)

        form = CsvImportForm()
        data = {"form": form, }

        return render (request, "admin/upload_csv.html", data)


class CurriculumAdmin(admin.ModelAdmin):
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
                return redirect("/admin/curriculum/subject/")

            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                created = Curriculum.objects.update_or_create(
                    id=row['id'],
                    year=row['year'],
                    course_id=row['course_id'],
                    subject_id=row['subject_id'],
                )
            url = reverse('admin:acad_subject_changelist')
            messages.success(request, 'Your csv file has been imported')
            return redirect(url)

        form = CsvImportForm()
        data = {"form": form, }

        return render (request, "admin/upload_csv.html", data)

# Register your models here.
admin.site.register(Course)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(StudentGrades)
admin.site.register(StudentProfile)