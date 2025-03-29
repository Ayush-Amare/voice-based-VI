from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from interview.models import InterviewSession
from .forms import LoginForm, RegisterForm, InterviewForm
from django.urls import reverse

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, "dashboard.html", {"username": request.user.username})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")   

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            next_url = request.GET.get("next", "dashboard")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "auth/login.html", {"form": form})

def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken!")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered!")
            elif len(password) < 6:
                messages.error(request, "Password must be at least 6 characters!")
            else:
                User.objects.create_user(username, email, password)
                messages.success(request, "Registration successful! Please log in.")
                return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("login") 

@login_required
def start_interview(request):
    return render(request, "start_interview.html")

@login_required
def interview_history(request):
    return render(request, "interview_history.html")

@login_required
def interview_setup(request):
    initial_data = {
        "full_name": request.user.get_full_name(),
        "email": request.user.email,
    } if request.user.is_authenticated else {}

    if request.method == "POST":
        form = InterviewForm(request.POST)
        if form.is_valid():
            job_title = form.cleaned_data["job_title"]
            difficulty_level = form.cleaned_data["difficulty_level"]

            request.session["interview_data"] = {
                "full_name": request.user.get_full_name(),
                "email": request.user.email,
                "job_title": job_title,
                "difficulty_level": difficulty_level,
            }
            return redirect("interview_start")
    else:
        form = InterviewForm(initial=initial_data)

    return render(request, "interview/interview_setup.html", {"form": form})

@login_required
def go_to_interview(request):
    return redirect(reverse('start_interview'))

@login_required
def past_interview(request):
    """Display a list of past interviews for the logged-in user."""
    sessions = InterviewSession.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "past_interview.html", {"sessions": sessions})

