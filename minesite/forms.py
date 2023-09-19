from django.forms import *
from minesite.models import LoginModel
from django.shortcuts import render

class LoginForm(Form):
    username = CharField(max_length=32)
    password = CharField(max_length=32, widget=PasswordInput)

    '''def cleaned_info(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        return {"username":username,"password":password} '''

class SignupForm(Form):
    name = CharField(max_length=32)
    username = CharField(max_length = 32)
    password = CharField(max_length = 32, widget=PasswordInput)
    confirmpassword = CharField(max_length = 32, widget = PasswordInput)
    email = EmailField()