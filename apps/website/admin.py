from django.contrib import admin
from .models import Specialization, Field, Skill, UserProfile, LearningMaterial
from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
from django.http import HttpResponse

from django.urls import path
from  django.urls import reverse

import csv


#class SuperuserOnlyFieldAdmin(admin.ModelAdmin):
    # Customizations for the Field model accessible only by superusers
    #list_display = ['field', 'field_name','description']  # Customize as needed
    #search_fields = ['field_name']  # Customize as needed
    # ... other customizations

    # def get_model_perms(self, request):
    #     perms = super().get_model_perms(request)
    #     if request.user.is_staff:
       
    #          perms.update({
    #             'view': False,
    #             'add': False,
    #             'change': False,
    #             'delete': False,
    #         })
    #          return perms
    #     return super().has_module_permission(request)

# admin.site.register(Field, SuperuserOnlyFieldAdmin)

class StaffOnlyFieldAdmin(admin.ModelAdmin):
    list_display = ['field', 'field_name','description']  # Customize as needed
    search_fields = ['field_name']  # Customize as needed
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_staff:
    #         return qs
    #     return qs.none()

# admin.site.register(Field, StaffOnlyFieldAdmin)

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()
    


class FieldAdmin(admin.ModelAdmin):
    list_display = ['field', 'field_name','description']  # Customize as needed
    search_fields = ['field_name']  # Customize as needed

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
                return redirect("/admin/website/field/")

            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                created = Field.objects.update_or_create(
                    field=row['field'], 
                    field_name=row['field_name'], 
                    description=row['description'],
                    explanation=row['explanation'],
                )
            url = reverse('admin:website_field_changelist')
            messages.success(request, 'Your csv file has been imported')
            return redirect(url)

        form = CsvImportForm()
        data = {"form": form, }

        return render (request, "admin/upload_csv.html", data)

class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['specialization_id', 'title','description']  # Customize as needed
    search_fields = ['title']  # Customize as needed

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

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
                return redirect("/admin/website/specialization/")
            
            field_names = [field.name for field in Specialization._meta.get_fields()]
            print("field_names:", field_names)

            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                created = Specialization.objects.update_or_create(
                    specialization_id=row['specialization_id'], 
                    title=row['title'], 
                    description=row['description'],
                    roadmap_id=row['roadmap_id'],
                    field_id=row['field_id']
                )
            url = reverse('admin:website_specialization_changelist')
            messages.success(request, 'Your csv file has been imported')
            return redirect(url)

        form = CsvImportForm()
        data = {"form": form, }

        return render (request, "admin/upload_csv.html", data)

class LearningMaterialAdmin(admin.ModelAdmin):
    list_display = ['material_id', 'title','description']  # Customize as needed
    search_fields = ['title']  # Customize as needed

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

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
                return redirect("/admin/website/learningmaterial/")
            
            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                created = LearningMaterial.objects.update_or_create(
                    material_id=row['material_id'], 
                    title=row['title'],
                    university=row['university'],
                    level=row['level'],
                    rating=row['rating'],
                    url=row['url'],
                    description=row['description'],
                    skills=row['skills'],
                    field_id=row['field_id']
                )
            url = reverse('admin:website_learningmaterial_changelist')
            messages.success(request, 'Your csv file has been imported')
            return redirect(url)

        form = CsvImportForm()
        data = {"form": form, }

        return render (request, "admin/upload_csv.html", data)


class StaffAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return False

class SuperuserAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

# Register your models here.

admin.site.register(Field, FieldAdmin)

admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Skill, SuperuserAdmin)
admin.site.register(UserProfile, SuperuserAdmin)
admin.site.register(LearningMaterial, LearningMaterialAdmin)
