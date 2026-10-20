from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.section_placeholder, {'section': 'dashboard'}, name='dashboard'),
path('calendar/', views.calendar, name='calendar'),
path('calendar/add/', views.calendar_add, name='calendar_add'),
path('calendar/<int:event_id>/edit/', views.calendar_edit, name='calendar_edit'),
path('calendar/<int:event_id>/delete/', views.calendar_delete, name='calendar_delete'),    path('study/', views.section_placeholder, {'section': 'study'}, name='study'),
    path('budget/', views.section_placeholder, {'section': 'budget'}, name='budget'),
    path('goals/', views.section_placeholder, {'section': 'goals'}, name='goals'),
    path('search/', views.section_placeholder, {'section': 'search'}, name='search'),
    path('canvas/', views.section_placeholder, {'section': 'canvas'}, name='canvas'),
]