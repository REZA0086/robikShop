from django import forms
from django.core.exceptions import ValidationError
from account.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "نام خود را وارد کنید"}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "آدرس ایمیل خود را وارد کنید"}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "پسورد خود را وارد کنید"}),
        }



class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "نام خود را وارد کنید"}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "پسورد خود را وارد کنید"}),
        }



