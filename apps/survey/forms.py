
from typing import Any
from django import forms
from .models import Survey

from apps.acad.models import StudentProfile, Course
from apps.website.models import Field

# class SurveyForm(forms.ModelForm):
#     class Meta:
#         model = Survey
#         exclude = ['user']  # Exclude the 'user' field from the form
#         widgets = {
#             'q1': forms.Select(attrs={'class': 'form-control'}),
#             'q2': forms.Select(attrs={'class': 'form-control'}),
#             'q3': forms.Select(attrs={'class': 'form-control'}),
#             'q4': forms.CheckboxInput(attrs={'class': 'form-check-input,d-block'}),
#             'q5': forms.Select(attrs={'class': 'form-control'}),
#             'q6': forms.Select(attrs={'class': 'form-control'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Add any additional customization or styling here if needed
#         self.fields['q1'].label = '1. What was your academic specialization?'

#     def save(self, commit=True, user=None, *args, **kwargs):
#         # Override the save method ts set the authenticated user before saving
#         instance = super(SurveyForm, self).save(commit=False, *args, **kwargs)

#         if user:
#             instance.user = user  # Set the user field to the authenticated user

#         if commit:
#             instance.save()

#         return instance


#   specialization = forms.ModelChoiceField(queryset=Field.objects.all())
        # field_names = Field.objects.values_list('field_name', flat=True)
        # SPECIALIZATION_CHOICES = [(field_name, field_name) for field_name in field_names]

        # specialization = forms.ChoiceField(choices=SPECIALIZATION_CHOICES)
        
        # widgets = {
        #     #'specialization': forms.Select(attrs={'class': 'form-control'}),
        #     #'received_recommendation': forms.Select(attrs={'class': 'form-control'}),
        #     #'explored_learning_materials': forms.Select(attrs={'class': 'form-control'}),
        #     #'accessed_job_postings': forms.Select(attrs={'class': 'form-control'}),
        # }
class SurveyForm(forms.ModelForm):
    
    class Meta:
        model = Survey
        fields = '__all__'
        exclude = ['user','acadmic_course','timestamp']

        # specialization = forms.CharField(
        #     widget=forms.Select, 
        #     choices=[(field.field, field.field_name) for field in Field.objects.all()])
        
    #specialization = forms.ModelChoiceField(queryset=Field.objects.all(), to_field_name='field_name')
    # # set label name 
    #specialization.label = '1. What specialization did you graduate with?'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['specialization'] = forms.ModelChoiceField(
            queryset=Field.objects.all(), 
            to_field_name='field_name',
            label='1. What specialization did you graduate with?',
            required=True,
        )
        self.fields['specialization'].required = True
        self.fields['employed'].required = True
        self.fields['received_recommendation'].required = True
        #self.fields['explored_learning_materials'].required = True
        #self.fields['accessed_job_postings'].required = True
        self.fields['additional_feedback'].required = False
        
        
        # specialization = forms.ModelChoiceField(queryset=Field.objects.all(), to_field_name='field_name')
        # field_choices = [(field.field, field.field_name) for field in Field.objects.all()]
        # self.fields['specialization'].choices = field_choices

        if user:
            student_profile = StudentProfile.objects.get(user_id=user)
            course = Course.objects.get(id=student_profile.enrolled_courses_id)
            self.fields['acad_course'].initial = course.course_name
    
        
    # def label_from_instance(self, obj):
    #     if isinstance(obj, Field):
    #         return obj.get_verbose_name()
    #     return super().label_from_instance(obj)

    def save(self, commit=True, user=None, *args, **kwargs):
        # Override the save method to set the authenticated user before saving
        instance = super(SurveyForm, self).save(commit=False, *args, **kwargs)

        if user:
            instance.user = user  # Set the user field to the authenticated user

        if commit:
            instance.save()

        return instance

    
# Additional form customization (optional)
    # Change field labels for clarity
    # Add help text for specific fields
    # Set initial values for certain fields
    # Define custom validation logic for specific fields


