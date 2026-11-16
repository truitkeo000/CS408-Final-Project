from .forms import AssignmentForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .forms import ExpenseForm
from .models import Expense
from .forms import StudentRegistrationForm, CalendarEventForm, StudySessionForm, AssignmentForm
from .models import StudentProfile, CalendarEvent, StudySession, Assignment


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

@login_required
def budget(request):
    expenses = Expense.objects.filter(
        student=request.user
    ).order_by('-expense_date')

    total = expenses.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    monthly_totals = (
        expenses.annotate(month=TruncMonth('expense_date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('-month')
    )

    category_totals = (
        expenses.values('category')
        .annotate(total=Sum('amount'))
        .order_by('category')
    )

    return render(request, 'core/budget.html', {
        'expenses': expenses,
        'total': total,
        'monthly_totals': monthly_totals,
        'category_totals': category_totals,
    })


@login_required
def budget_add(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.student = request.user
            expense.save()
            return redirect('budget')
    else:
        form = ExpenseForm()

    return render(request, 'core/budget_form.html', {
        'form': form,
        'page_title': 'Add Expense',
    })


@login_required
def budget_edit(request, expense_id):
    expense = get_object_or_404(
        Expense,
        id=expense_id,
        student=request.user
    )

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('budget')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'core/budget_form.html', {
        'form': form,
        'page_title': 'Edit Expense',
    })


@login_required
@require_POST
def budget_delete(request, expense_id):
    expense = get_object_or_404(
        Expense,
        id=expense_id,
        student=request.user
    )
    expense.delete()
    return redirect('budget')


@login_required
@require_POST
def calendar_toggle_complete(request, event_id):
    event = get_object_or_404(
        CalendarEvent,
        id=event_id,
        student=request.user
    )
    event.completed = not event.completed
    event.save(update_fields=['completed'])
    return redirect('calendar')


@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        student=request.user
    )

    return render(
        request,
        'core/assignment_detail.html',
        {'assignment': assignment}
    )


@login_required
def assignment_list(request):
    assignments = Assignment.objects.filter(student=request.user)

    q = request.GET.get('q', '').strip()
    course = request.GET.get('course', '').strip()
    status = request.GET.get('status', '').strip()

    if q:
        assignments = assignments.filter(title__icontains=q)

    if course:
        assignments = assignments.filter(course__iexact=course)

    if status == 'completed':
        assignments = assignments.filter(completed=True)
    elif status == 'incomplete':
        assignments = assignments.filter(completed=False)

    courses = (
        Assignment.objects.filter(student=request.user)
        .order_by('course')
        .values_list('course', flat=True)
        .distinct()
    )

    return render(request, 'core/assignment_list.html', {
        'assignments': assignments.order_by('due_date'),
        'courses': courses,
        'q': q,
        'selected_course': course,
        'selected_status': status,
    })


@login_required
def assignment_add(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = request.user
            assignment.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm()

    return render(
        request,
        'core/assignment_form.html',
        {'form': form}
    )


@login_required
@require_POST
def assignment_toggle_complete(request, assignment_id):
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        student=request.user
    )
    assignment.completed = not assignment.completed
    assignment.save(update_fields=['completed'])
    return redirect('assignment_list')


@login_required
@require_POST
def assignment_delete(request, assignment_id):
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        student=request.user
    )
    assignment.delete()
    return redirect('assignment_list')


from .models import Goal
from .forms import GoalForm


@login_required
def goals(request):
    user_goals = Goal.objects.filter(
        student=request.user
    ).order_by('-created_at')

    return render(request, 'core/goals.html', {
        'goals': user_goals,
    })


@login_required
def goal_add(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.student = request.user
            goal.save()
            return redirect('goals')
    else:
        form = GoalForm()

    return render(request, 'core/goal_form.html', {
        'form': form,
        'page_title': 'Add Goal',
    })


@login_required
def goal_edit(request, goal_id):
    goal = get_object_or_404(
        Goal,
        id=goal_id,
        student=request.user
    )

    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goals')
    else:
        form = GoalForm(instance=goal)

    return render(request, 'core/goal_form.html', {
        'form': form,
        'page_title': 'Edit Goal',
    })


@login_required
@require_POST
def goal_delete(request, goal_id):
    goal = get_object_or_404(
        Goal,
        id=goal_id,
        student=request.user
    )
    goal.delete()
    return redirect('goals')


@login_required
def dashboard(request):
    today = timezone.localdate()
    now = timezone.now()

    # Upcoming calendar events
    upcoming_events = CalendarEvent.objects.filter(
        student=request.user,
        starts_at__gte=now,
        completed=False
    ).order_by('starts_at')[:5]

    # Study time for the current week (Monday-Sunday)
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    study_minutes = StudySession.objects.filter(
        student=request.user,
        study_date__range=(week_start, week_end)
    ).aggregate(
        total=Sum('duration_minutes')
    )['total'] or 0

    # Current goals
    current_goals = Goal.objects.filter(
        student=request.user
    ).order_by('-created_at')[:5]

    # Expenses for the current month
    monthly_expenses = Expense.objects.filter(
        student=request.user,
        expense_date__year=today.year,
        expense_date__month=today.month
    ).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    return render(request, 'core/dashboard.html', {
        'upcoming_events': upcoming_events,
        'study_minutes': study_minutes,
        'current_goals': current_goals,
        'monthly_expenses': monthly_expenses,
        'current_month': today.strftime('%B %Y'),
    })
