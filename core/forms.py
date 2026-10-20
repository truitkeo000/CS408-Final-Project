from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from .models import CalendarEvent


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