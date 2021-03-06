from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Profile


class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(error_messages={'required': 'Please enter your username or email address'})
    password = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={'required': 'Please enter your password'}
    )



class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        error_messages={'required': 'Please enter a valid password'}
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
        error_messages={'required': 'Please confirm your password'}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError("Password must not be empty")

        if password1 != password2:
            raise ValidationError("Passwords do not match")

        return password2


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio', 'location', 'profile_pic')
