from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        min_length=6,  # Password must be at least 6 chars
        error_messages={"min_length": "Password must be at least 6 characters!"},
    )

class InterviewForm(forms.Form):
    full_name = forms.CharField(label="Full Name", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    job_title = forms.CharField(label="Job Title", max_length=100, required=True)
    difficulty_level = forms.ChoiceField(
        label="Difficulty Level",
        choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")],
        required=True
    )
