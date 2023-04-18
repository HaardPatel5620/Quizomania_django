from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# class createuserform(UserCreationForm):
#     class Meta:
#         model=User
#         fields=['username','password'] 

class createuserform(UserCreationForm):
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        # labels = {"email": "Email"}
        widgets = {"username": forms.TextInput(attrs={"class": "form-control"})}


class addQuestionform(ModelForm):
    class Meta:
        model=QuesModel
        fields="__all__"
    