from django.contrib import admin
from django.urls import path, include
from Home import views
import interview
import interview.urls
from interview.views import evaluate_interview, start_interview
from .views import dashboard, user_login, user_register, user_logout,interview_setup,past_interview

urlpatterns = [
    path('', views.home , name="home"),

    path('about/', views.about , name="about"),

    path('contact/', views.contact , name="contact"),

    path("login/", user_login, name="login"),

    path("register/", user_register, name="register"),

    path("dashboard/", dashboard, name="dashboard"),

    path("logout/", user_logout, name="logout"),

    path("past_interview/", past_interview,name="past_interview"),
    
    path('setup/', include('interview.urls')),
]
