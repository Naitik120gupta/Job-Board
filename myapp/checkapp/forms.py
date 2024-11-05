from .models import User,JobPosting
from django import forms
from allauth.account.forms import SignupForm

# from captcha.fields import ReCaptchaField

# class CustomSignupForm(SignupForm):
#     captcha = ReCaptchaField()
#     def signup(self, request, user):
#         return super().signup(request, user)

# jobboard/forms.py

class JobUpdateForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['job_title', 'job_description', 'location', 'salary', 'application_deadline', 'status']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'account_type']
