from django import forms
from django.utils import timezone

from .models import Project, Client


class ClientForm(forms.Form):
    name = forms.CharField()


class ProjectForm(forms.Form):
	name = forms.CharField()
	client = forms.ModelChoiceField(queryset=Client.objects.all())


class EntryForm(forms.Form):
    start = forms.DateTimeField(label="Start Time", help_text="Format: 2006-10-25 14:30")
    stop = forms.DateTimeField(label="End Time", help_text="Format: 2006-10-25 14:30")
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    description = forms.CharField()

    def clean_start(self):
        """
        Validation for start field
        """
        start = self.cleaned_data['start']
        if start >= timezone.now():
            raise forms.ValidationError('Start time must be in the past')

        # Must return the value, regardless of whether we changed it or not
        return start

    def clean(self):
        """
        This method handles the validation of the form overall and is useful for
        handling scenarios like when a field relies on another field
        """
        # Call parent's clean method to ensure any validation logic in parent class
        # is preserved
        cleaned_data = super(EntryForm, self).clean()

        # Get the start and end values from the cleaned_data dictionary, or None
        # if the dictionary keys are missing
        start = cleaned_data.get('start', None)
        end = cleaned_data.get('end', None)

        if end and start and (end < start):
            raise forms.ValidationError('End time must come after start time')
        # No need to return anything (Django 1.7 and above)
