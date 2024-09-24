from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class UserRegisterForm(UserCreationForm):
    email =  forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1', 'password2']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['head_image']
    

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password']