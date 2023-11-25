from django.contrib import admin
from .models import Test, QuestionSet, UserResponse
from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
from django.http import HttpResponse

from django.urls import path
from  django.urls import reverse

import csv


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()
    

class TestAdmin(admin.ModelAdmin):
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
                return redirect("/admin/assessment/test/")

            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                created = Test.objects.update_or_create(
                    question_id=row['question_id'],
                    question=row['question'],
                    description=row['description'],
                    options=row['options'],
                    correct_option=row['correct_option'],
                    field_id=row['field_id'],
                )
            url = reverse('admin:assessment_test_changelist')
            messages.success(request, 'Your csv file has been imported')
            return redirect(url)

        form = CsvImportForm()
        data = {"form": form, }

        return render (request, "admin/upload_csv.html", data)


# Register your models here.
admin.site.register(Test, TestAdmin)
admin.site.register(QuestionSet)
admin.site.register(UserResponse)

