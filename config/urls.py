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
    path('dashboard/', views.section_placeholder,
         {'section': 'dashboard'}, name='dashboard'),

    # Calendar
    path('calendar/', views.calendar, name='calendar'),
    path('calendar/add/', views.calendar_add, name='calendar_add'),
    path('calendar/<int:event_id>/edit/',
         views.calendar_edit, name='calendar_edit'),
    path('calendar/<int:event_id>/delete/',
         views.calendar_delete, name='calendar_delete'),

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
    path('goals/', views.section_placeholder,
         {'section': 'goals'}, name='goals'),
    path('search/', views.section_placeholder,
         {'section': 'search'}, name='search'),
    path('canvas/', views.section_placeholder,
         {'section': 'canvas'}, name='canvas'),
]
