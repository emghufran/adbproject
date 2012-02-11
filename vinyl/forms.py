from adbproject.ajax_select import make_ajax_field
from adbproject.vinyl.models import *
from django import forms
#from django.db import models
#from django.contrib.auth.models import User
#from django.contrib import admin
#from django.contrib.auth.forms import UserCreationForm
#from adbproject import settings

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

class RecordForm(forms.ModelForm):
	matrix_number = forms.CharField(max_length=64, required=True)
	title = forms.CharField(max_length=128, required=False)
	DISC_SIZES = (('7','7 inches'), ('10','10 inches'), ('12','12 inches'))
	PRESS_INFO = (('first','first'), ('repress','repress'))
	disk_size = forms.ChoiceField(choices=DISC_SIZES, required=False)
	press_info = forms.ChoiceField(choices=PRESS_INFO, required=False)
		
	#make_ajax_field(model,model_fieldname,channel,show_help_text = False,**kwargs)
	genre = make_ajax_field(Record,'genre','genre') #,help_text=True)
	artist = make_ajax_field(Record,'artist','artist') #,help_text=True)
	category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=1)
	class Meta:
		model = Record
		fields = ('matrix_number', 'title', 'disk_size', 'press_info', 'genre', 'artist', 'category')
		#exclude = ('user_id')

class RecordArchiveForm(forms.ModelForm):
	matrix_number = forms.CharField(max_length=64, required=True)
	title = forms.CharField(max_length=128, required=False)
	DISC_SIZES = (('7','7 inches'), ('10','10 inches'), ('12','12 inches'))
	PRESS_INFO = (('first','first'), ('repress','repress'))
	disk_size = forms.ChoiceField(choices=DISC_SIZES, required=False)
	press_info = forms.ChoiceField(choices=PRESS_INFO, required=False)
		
	#make_ajax_field(model,model_fieldname,channel,show_help_text = False,**kwargs)
	genre = forms.IntegerField(required=False)
	artist = forms.IntegerField(required=False)
	category = forms.IntegerField(required=False)
	class Meta:
		model = RecordArchive
		fields = ('matrix_number', 'title', 'disk_size', 'press_info', 'genre', 'artist', 'category')
		
class SearchForm(forms.Form):
	record_title = forms.CharField(max_length=128, required=False)
	artist = forms.CharField(max_length=128, required=False)
	rating_lower = forms.ChoiceField(widget = forms.Select(), 
                 choices = ([('',''), ('1','1'), ('2','2'),('3','3'), ('4','4'),('5','5')]), required=False)
	rating_upper  = forms.ChoiceField(widget = forms.Select(), 
                 choices = ([('',''), ('1','1'), ('2','2'),('3','3'), ('4','4'),('5','5')]), required=False)
	
	genre = forms.CharField(required=False)
	category = forms.CharField(required=False)

class SoundtrackForm(forms.ModelForm):
	title = forms.CharField(max_length=256, required=True)
	artist = make_ajax_field(Trackartist,'artist','artist',help_text="Primary artist")
	
	release_date = forms.CharField(required=False)
	playing_time = forms.IntegerField(required=False)
	style = forms.CharField(max_length=128, required=False)
	audio_engineer = forms.CharField(max_length=128, required=False)
	lyricist = forms.CharField(max_length=128, required=False)
	music_writer = forms.CharField(max_length=128, required=False)
	rythm = forms.CharField(max_length=128, required=False)
	label = forms.CharField(max_length=128, required=False)
	genre = make_ajax_field(Record,'genre','genre', required=False) #,help_text=True)
	
	original_version = make_ajax_field(Recordtrack,'track','soundtrack_title',help_text="Search for existing soundtracks", required=False)
	player = make_ajax_field(Soundtrack,'player','musicplayer_name', required=False)#,help_text="Add music players")
	#player = models.ManyToManyField(Musicplayer)
	class Meta:
		model = Soundtrack

class RecordtrackForm(forms.ModelForm):
	#make_ajax_field(model,model_fieldname,channel,show_help_text = False,**kwargs)
	track = make_ajax_field(Recordtrack,'track','soundtrack_title',help_text="Search for existing soundtracks or add a new using link at the top")
	order = forms.CharField(max_length=32, required=True)
	disc_number = forms.IntegerField(required=True)
		
	class Meta:
		model = Recordtrack
		fields = ('track', 'order', 'disc_number')

class RecordtrackSmallForm(forms.ModelForm):
	#make_ajax_field(model,model_fieldname,channel,show_help_text = False,**kwargs)
	order = forms.CharField(max_length=32, required=True, help_text="Order of the track in the record")
	disc_number = forms.IntegerField(required=True, help_text="Disc number in the record")
		
	class Meta:
		model = Recordtrack
		fields = ('order', 'disc_number')
