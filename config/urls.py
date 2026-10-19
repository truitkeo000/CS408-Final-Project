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
    path('calendar/', views.section_placeholder, {'section': 'calendar'}, name='calendar'),
    path('study/', views.section_placeholder, {'section': 'study'}, name='study'),
    path('budget/', views.section_placeholder, {'section': 'budget'}, name='budget'),
    path('goals/', views.section_placeholder, {'section': 'goals'}, name='goals'),
    path('search/', views.section_placeholder, {'section': 'search'}, name='search'),
    path('canvas/', views.section_placeholder, {'section': 'canvas'}, name='canvas'),
]