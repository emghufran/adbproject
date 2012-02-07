from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from adbproject import settings
from adbproject.vinyl.models import *
#UserProfile form	
class UserProfileForm(forms.ModelForm):
	mid_name = forms.CharField(max_length=128, required=False)
	phone = forms.CharField(max_length=32, required=False)
	address = forms.CharField(max_length=512, required=False)
	#language = forms.CharField(max_length=128, required=False)
	language = forms.ChoiceField(choices=settings.SUPPORTED_LANGUAGES, initial='en', required=False)
	profile_pic = forms.CharField(max_length=512, required=False)
	class Meta:
		model = UserProfile
		exclude = ('user_id')

class RegisterForm(UserCreationForm):
	username = forms.RegexField(label= "Username" , max_length = 30, regex = r'^[\w]+$', error_messages = {'invalid': "This value may contain only letters, numbers and _ characters."})
	email = forms.EmailField(label = "Email")
	first_name = forms.CharField(label = "First name", required = True)
	last_name = forms.CharField(label = "Last name", required = True)
	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "email")

	def save(self, commit = True):
		user = super(RegisterForm, self).save(commit = False)
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user

	def clean_email(self):
		data = self.cleaned_data['email']
		if User.objects.filter(email=data).exists():
			raise forms.ValidationError("This email already used")
		return data
