from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta

from .forms import StudentRegistrationForm, CalendarEventForm, StudySessionForm
from .models import StudentProfile, CalendarEvent, StudySession


def home(request):
    return render(request, 'core/home.html')


def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = StudentRegistrationForm()

    return render(request, 'core/register.html', {'form': form})


@login_required
def profile(request):
    student_profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        'core/profile.html',
        {'student_profile': student_profile}
    )

@login_required
def section_placeholder(request, section):
    sections = {
        'dashboard': 'Dashboard',
        'calendar': 'Calendar',
        'study': 'Study Log',
        'budget': 'Budget',
        'goals': 'Goals',
        'search': 'Conditional Search',
        'canvas': 'Canvas Integration',
    }
    return render(request, 'core/placeholder.html', {
        'section_name': sections[section]
    })

@login_required
def calendar(request):
    events = CalendarEvent.objects.filter(
        student=request.user
    ).order_by('starts_at')

    today = timezone.now()

    for event in events:
        deadline = event.ends_at or event.starts_at

        if event.completed:
            event.status = 'Completed'
            event.status_color = 'secondary'
        elif deadline < today:
            event.status = 'Overdue'
            event.status_color = 'danger'
        else:
            days_left = (
                timezone.localtime(deadline).date()
                - timezone.localdate()
            ).days

            if days_left <= 3:
                event.status = 'Urgent'
                event.status_color = 'danger'
            elif days_left <= 7:
                event.status = 'Upcoming'
                event.status_color = 'warning'
            else:
                event.status = 'On Track'
                event.status_color = 'success'

    return render(request, 'core/calendar.html', {
        'events': events,
        'form': CalendarEventForm(),
    })



@login_required
def calendar_add(request):
    if request.method == 'POST':
        form = CalendarEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.student = request.user
            event.save()
            return redirect('calendar')
    else:
        form = CalendarEventForm()

    return render(request, 'core/calendar_form.html', {
        'form': form,
        'page_title': 'Add Event',
    })


@login_required
def calendar_edit(request, event_id):
    event = get_object_or_404(
        CalendarEvent,
        id=event_id,
        student=request.user
    )

    if request.method == 'POST':
        form = CalendarEventForm(request.POST, instance=event)

        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = CalendarEventForm(instance=event)

    return render(request, 'core/calendar_form.html', {
        'form': form,
        'event': event,
    })


@login_required
@require_POST
def calendar_delete(request, event_id):
    event = get_object_or_404(
        CalendarEvent,
        id=event_id,
        student=request.user
    )
    event.delete()
    return redirect('calendar')


# Study Log views

@login_required
def study_log(request):
    sessions = StudySession.objects.filter(
        student=request.user
    ).order_by('-study_date', '-created_at')

    # Calculate total study minutes for the current week.
    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=7)

    weekly_sessions = sessions.filter(
        study_date__gte=week_start,
        study_date__lt=week_end
    )

    weekly_minutes = sum(
        session.duration_minutes for session in weekly_sessions
    )

    weekly_hours = round(weekly_minutes / 60, 2)

    return render(request, 'core/study_log.html', {
        'sessions': sessions,
        'weekly_minutes': weekly_minutes,
        'weekly_hours': weekly_hours,
    })


@login_required
def study_add(request):
    if request.method == 'POST':
        form = StudySessionForm(request.POST)

        if form.is_valid():
            session = form.save(commit=False)
            session.student = request.user
            session.save()
            return redirect('study')
    else:
        form = StudySessionForm()

    return render(request, 'core/study_form.html', {
        'form': form,
        'page_title': 'Add Study Session',
    })


@login_required
def study_edit(request, session_id):
    session = get_object_or_404(
        StudySession,
        id=session_id,
        student=request.user
    )

    if request.method == 'POST':
        form = StudySessionForm(request.POST, instance=session)

        if form.is_valid():
            form.save()
            return redirect('study')
    else:
        form = StudySessionForm(instance=session)

    return render(request, 'core/study_form.html', {
        'form': form,
        'page_title': 'Edit Study Session',
    })


@login_required
@require_POST
def study_delete(request, session_id):
    session = get_object_or_404(
        StudySession,
        id=session_id,
        student=request.user
    )

    session.delete()
    return redirect('study')
