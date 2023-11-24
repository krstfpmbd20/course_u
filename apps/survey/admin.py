from django.contrib import admin
from .models import Survey

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('user', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', )
    search_fields = ('q1', 'q2', 'q3', 'q5', 'q6', 'user')  # Add any other fields you want to search on

admin.site.register(Survey, SurveyAdmin)
