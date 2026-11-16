from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    school_name = models.CharField(max_length=120, blank=True)
    canvas_base_url = models.URLField(blank=True)
    canvas_token_encrypted = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class CalendarEvent(models.Model):
    EVENT_TYPES = [
        ('academic', 'Academic'),
        ('work', 'Work'),
        ('personal', 'Personal'),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='calendar_events'
    )
    title = models.CharField(max_length=160)
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES
    )
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(
        null=True,
        blank=True
    )
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class StudySession(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='study_sessions'
    )
    subject = models.CharField(max_length=120)
    study_date = models.DateField()
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.study_date}"
    
class Expense(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.CharField(max_length=30)
    expense_date = models.DateField()
    description = models.CharField(max_length=180)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category}: ${self.amount}"


class Assignment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    title = models.CharField(max_length=160)
    course = models.CharField(max_length=120)
    due_date = models.DateTimeField()
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course}: {self.title}"


class Goal(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='goals'
    )
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    target_value = models.PositiveIntegerField()
    current_value = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def progress_percentage(self):
        if self.target_value == 0:
            return 0
        return min(100, round(
            (self.current_value / self.target_value) * 100
        ))

    def __str__(self):
        return self.title
