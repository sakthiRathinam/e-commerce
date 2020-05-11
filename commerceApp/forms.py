from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
class UserForm(UserCreationForm):
	class Meta:
		model=User
		fields=['username','email','password1','password2']
class CustomerForm(ModelForm):
	class Meta:
		model=Customer
		fields=['user','name','email']
class UpdateForm(ModelForm):
	class Meta:
		model=Customer
		fields=['name','email','image']