from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import StudentRegistrationForm
from .models import StudentProfile


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