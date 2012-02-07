from adbproject import settings
from adbproject.vinyl.models import *

from django.contrib.auth import logout, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.utils.translation import activate
from django.views.generic.list_detail import object_list

from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

import logging
logger = logging.getLogger(__name__)

def homepage(request):
	record_list = Record.objects.all()

	return object_list(request, template_name = 'index.html',
         queryset = record_list, paginate_by = 12)
#	records = Record.objects.all()
#	t = loader.get_template('index.html')
#	
#	p = Paginator(records, 15)
#	data =  p.page(1)
#	c = RequestContext(request, {'records': data, 'paginator': p})
#	return HttpResponse(t.render(c))
	
def playlists(request, pltype):
	from django.contrib.auth import get_user
	curuser = get_user(request)
	user = User.objects.get(id=curuser.id)
		
	if (pltype == 'my'):
		playlists = user.playlist_set.all()
	elif (pltype == 'sharedwm'):
		playlists = user.shared_user.all()
	elif (pltype == 'myshared'):
		playlists = user.owner.all()
	else:
		pltype = 'all'
		playlists = Playlist.objects.all()
	
	return object_list(request, template_name = 'playlists.html',
         queryset = playlists, paginate_by = 10)
#    t = loader.get_template("playlists.html")
#    c = RequestContext(request, {})
#    response = HttpResponse(t.render(c))
#    return response
	

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		profile_form = UserProfileForm(request.POST)
		if form.is_valid() and profile_form.is_valid():
			#do something
			logger.debug("testing register: if case")
			user = form.save()
			user_profile = profile_form.save(commit=False)
			user_profile.user_id = user.id
			user_profile.save()
			import md5
			m = md5.new(user.username)
			email_text = "Dear " + user.username + ",\n\nWe welcome you to VinylRecords. Please click on the following link to confirm your registration:\n\n" + settings.SITE_BASE_URL + "accounts/activate/" + str(user.id) + "/" + m.hexdigest() + "\n\nThanks,\nVinylRecords Team."
			send_mail('Welcome to Vinyl Records', email_text, 'admin@vinylrecords.com', [user.email])
			return HttpResponseRedirect('/vinyl/playlists/all/')
	else:
		form = RegisterForm()
		profile_form = UserProfileForm()
		
	return render_to_response('registration/register.html', { 'form' : form, 'profile_form': profile_form }, context_instance=RequestContext(request))
		
def my_test_view(request):
	send_mail('Subject', 'Message. ', 'from@example.com', ['emghufran@gmail.com'])
	t = loader.get_template("my_test_view.html")
	c = RequestContext(request, {})
	return HttpResponse(t.render(c))

def change_language(request, lang):
	activate(lang)
	response = HttpResponse()
	response.set_cookie('django_language', lang)
	response.write(True)
	return response

def record_details(request, record_id):
	record = Record.objects.get(id=record_id)
	rating = record.rating_set.all()
	recordtracks = record.recordtrack_set.all()
#  	data = list(record.recordtrack_set.all(), Soundtrack.objects.all())
#  	print data.count()
	artists = {}
	data = []
	for recordtrack in recordtracks:
		trackartist_list = recordtrack.track.trackartist_set.all()
		artiststr = []
		for trackartist in trackartist_list:
			artiststr.append(trackartist.artist.name)
		data.append({'recordtrack':recordtrack, 'artists': ",".join(artiststr) })
		
			
	comments = record.comment_set.all()
	
#  	rating = Rating.objects.get(record=record_id) 
	
	t = loader.get_template("record_details.html")
	c = RequestContext(request, {'record': record, 'rating':rating, 'comments': comments, 'data': data, 'recordtracks': recordtracks, 'artists': artists})
	return HttpResponse(t.render(c))

def playlist_details(request, playlist_id):
	playlist = Playlist.objects.get(id=playlist_id)
	playlistitems = playlist.playlistitem_set.all()
	shares = playlist.playlistshare_set.all()
	
	t = loader.get_template("playlist_details.html")
	c = RequestContext(request, {'playlist': playlist, 'shares': shares, 'playlistitems': playlistitems})
	return HttpResponse(t.render(c))

def track_details(request, track_id):
	track = Soundtrack.objects.get(id=track_id)
	artists = track.trackartist_set.all()
	musicplayers = track.player.all()
	
	artiststr = []
	feat_artiststr = []
	for artist in artists:
		if artist.type == 'M':
			artiststr.append(artist.name)
		elif artists.type == 'F':
			feat_artiststr.append(artist.name)

	playerstr = []
	for player in musicplayers:
		playerstr.append(player.player_name)
		
	t = loader.get_template("track_details.html")
	c = RequestContext(request, {'track': track, 'artists': ",".join(artiststr), 'feat_artists': ",".join(feat_artiststr),'musicplayers': ",".join(playerstr)})
	return HttpResponse(t.render(c))

# TODO update these views. They are added to make navigation work.
def edit_track(request, track_id):
	return HttpResponse("")

def edit_playlist(request, playlist_id):
	return HttpResponse("")

def edit_record(request, record_id):
	return HttpResponse("")

