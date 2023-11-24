from django import forms
from .models import Survey

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        exclude = ['user']  # Exclude the 'user' field from the form
        widgets = {
            'q1': forms.Select(attrs={'class': 'form-control'}),
            'q2': forms.Select(attrs={'class': 'form-control'}),
            'q3': forms.Select(attrs={'class': 'form-control'}),
            'q4': forms.CheckboxInput(attrs={'class': 'form-check-input,d-block'}),
            'q5': forms.Select(attrs={'class': 'form-control'}),
            'q6': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add any additional customization or styling here if needed
        self.fields['q1'].label = '1. What was your academic specialization?'

    def save(self, commit=True, user=None, *args, **kwargs):
        # Override the save method to set the authenticated user before saving
        instance = super(SurveyForm, self).save(commit=False, *args, **kwargs)

        if user:
            instance.user = user  # Set the user field to the authenticated user

        if commit:
            instance.save()

        return instance
