from django.contrib.auth.forms import AuthenticationForm
from django import forms

# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'email'}))

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="old password", max_length=8,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'old_password'}))
    new_password = forms.CharField(label="new password", max_length=8,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'new_password'}))
    confirm_password = forms.CharField(label="confirm password", max_length=8,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'confirm_password'}))


class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(label="first_name", max_length=8,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name'}))
    last_name = forms.CharField(label="last_name", max_length=8,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name'}))
    phone_number = forms.CharField(label="phone_number", max_length=39,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'phone_number'}))
