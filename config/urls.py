from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Calendar
    path('calendar/', views.calendar, name='calendar'),
    path('calendar/add/', views.calendar_add, name='calendar_add'),
    path('calendar/<int:event_id>/edit/',
         views.calendar_edit, name='calendar_edit'),
    path('calendar/<int:event_id>/delete/',
         views.calendar_delete, name='calendar_delete'),

    path('calendar/<int:event_id>/toggle/',
         views.calendar_toggle_complete,
         name='calendar_toggle_complete'),

    # Assignments
    path('assignments/',
         views.assignment_list,
         name='assignment_list'),

    path('assignments/add/',
         views.assignment_add,
         name='assignment_add'),

    # Assignment Details
    path('assignments/<int:assignment_id>/',
         views.assignment_detail,
         name='assignment_detail'),

    path('assignments/<int:assignment_id>/toggle/',
         views.assignment_toggle_complete,
         name='assignment_toggle_complete'),

    path('assignments/<int:assignment_id>/delete/',
         views.assignment_delete,
         name='assignment_delete'),

    # Study Log
    path('study/', views.study_log, name='study'),
    path('study/add/', views.study_add, name='study_add'),
    path('study/<int:session_id>/edit/',
         views.study_edit, name='study_edit'),
    path('study/<int:session_id>/delete/',
         views.study_delete, name='study_delete'),

     # Budget
     path('budget/', views.budget, name='budget'),
     path('budget/add/', views.budget_add, name='budget_add'),
     path('budget/<int:expense_id>/edit/',
          views.budget_edit, name='budget_edit'),
     path('budget/<int:expense_id>/delete/',
          views.budget_delete, name='budget_delete'),

    # Future sections
    path('goals/', views.goals, name='goals'),
    path('goals/add/', views.goal_add, name='goal_add'),
    path('goals/<int:goal_id>/edit/',
         views.goal_edit, name='goal_edit'),
    path('goals/<int:goal_id>/delete/',
         views.goal_delete, name='goal_delete'),
    path('search/', views.section_placeholder,
         {'section': 'search'}, name='search'),
    path('canvas/', views.section_placeholder,
         {'section': 'canvas'}, name='canvas'),
]
