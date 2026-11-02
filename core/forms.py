from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from .models import CalendarEvent, StudySession

class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = [
            'title',
            'event_type',
            'starts_at',
            'ends_at',
            'notes',
            'completed',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event title'
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'starts_at': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'ends_at': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['starts_at'].input_formats = [
            '%Y-%m-%dT%H:%M'
        ]
        self.fields['ends_at'].input_formats = [
            '%Y-%m-%dT%H:%M'
        ]

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('starts_at')
        end = cleaned_data.get('ends_at')

        if start and end and end < start:
            self.add_error(
                'ends_at',
                'End date cannot be before start date.'
            )

        return cleaned_data

class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = [
            'subject',
            'study_date',
            'duration_minutes',
            'notes',
        ]

        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject or course'
            }),
            'study_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Minutes studied'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What did you study?'
            }),
        }

    def clean_duration_minutes(self):
        duration = self.cleaned_data['duration_minutes']

        if duration < 1:
            raise forms.ValidationError(
                'Study duration must be at least 1 minute.'
            )

        return duration
