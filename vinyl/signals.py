from django.db import models
from django.db.models.signals import post_save
from adbproject.vinyl.models import UserProfile

def login_set_lang_cookie(sender, **kw):
	lang = sender.language
	request.session["language"] = lang
	#response.set_cookie('django_language', lang)
