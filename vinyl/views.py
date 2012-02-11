from adbproject import settings
from adbproject.vinyl.forms import *
from adbproject.vinyl.models import *
from adbproject.vinyl.snippets.tablesorter import SortHeaders
from adbproject.vinyl.utils import get_query, pluralize
from datetime import datetime
from django.contrib.auth import logout, logout, logout, get_user
from django.contrib.auth.forms import UserCreationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail, send_mail
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models.aggregates import Count
from django.db.utils import IntegrityError
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.utils.translation import activate
from django.views.generic.list_detail import object_list
import logging
import urllib

#from haystack.views import SearchView


logger = logging.getLogger('django.request')

def homepage(request):
	record_list = Record.objects.all()

	return object_list(request, template_name='index.html',
         queryset=record_list, paginate_by=12)
	
def playlists(request, pltype):
	user = get_user(request)
	
	LIST_HEADERS = (
				('Playlist', 'list_name'),
				('Created by', 'created_by__username'),
				('Created on', 'created_on'),
				('# of Records', 'num_records'),
				)
		
	sort_headers = SortHeaders(request, LIST_HEADERS)
	if (pltype == 'my'):
		playlists = Playlist.objects.filter(created_by__id=user.id)\
							.annotate(num_records=Count('playlistitem')).order_by(sort_headers.get_order_by())
	elif (pltype == 'sharedwm'):
		playlists = Playlist.objects.filter(playlistshare__shared_to__id=user.id)\
							.annotate(num_records=Count('playlistitem')).order_by(sort_headers.get_order_by())
	elif (pltype == 'myshared'):
		playlists = Playlist.objects.filter(playlistshare__created_by__id=user.id)\
							.annotate(num_records=Count('playlistitem')).order_by(sort_headers.get_order_by())
	else:
		pltype = 'all'
		playlists = Playlist.objects.annotate(num_records=Count('playlistitem'))\
							.order_by(sort_headers.get_order_by())
			
	return object_list(request, template_name='playlists.html',
         queryset=playlists, paginate_by=10, extra_context={'ptype':pltype, 'headers': list(sort_headers.headers())})
	

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
	artists = {}
	data = []
	recordtrack_form = RecordtrackForm()
	for recordtrack in recordtracks:
		trackartist_list = recordtrack.track.trackartist_set.all()
		artiststr = []
		for trackartist in trackartist_list:
			artiststr.append(trackartist.artist.name)
		data.append({'recordtrack':recordtrack, 'artists': ",".join(artiststr) })
		
			
	comments = record.comment_set.all()
	
#  	rating = Rating.objects.get(record=record_id) 
	
	t = loader.get_template("record_details.html")
	c = RequestContext(request, {'record': record, 'rating':rating, 'comments': comments, \
								'data': data, 'recordtracks': recordtracks, 'artists': artists, \
								'recordtrack_form' : recordtrack_form})
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
	c = RequestContext(request, {'track': track, 'artists': ",".join(artiststr), \
								'feat_artists': ",".join(feat_artiststr), 'musicplayers': ",".join(playerstr)})
	return HttpResponse(t.render(c))

# TODO update these views. They are added to make navigation work.
def edit_track(request, track_id):
	return HttpResponse("")

def new_track(request, record_id):
	if request.method == 'POST':
		if Record.objects.filter(pk=record_id).count() < 1:
			return HttpResponseRedirect('/') #do something better
		
		form = SoundtrackForm(request.POST)
		recordtrack = RecordtrackSmallForm(request.POST)
		
		if form.is_valid() and recordtrack.is_valid():
			artist = request.POST['artist']
			soundtrack = form.save()
			print soundtrack.id
			if Trackartist.objects.filter(artist__id=artist,track__id=soundtrack.id).count() < 1:
				Trackartist.objects.create(artist_id=artist, track_id=soundtrack.id,artisttype="P")
			
			rt = recordtrack.save(commit=False)
			if Recordtrack.objects.filter(record__id=record_id, track__id=soundtrack.id).count() < 1:
				rt.record_id = record_id
				rt.track_id = soundtrack.id
				rt.save()
			logger.debug("testing register: if case")
			return HttpResponseRedirect('/vinyl/record/' + str(record_id))
	else:
		form = SoundtrackForm()
		recordtrack = RecordtrackSmallForm()
		
	return render_to_response('record/new_track.html', { 'form' : form, 'record':record_id, 'recordtrack':recordtrack }, context_instance=RequestContext(request))

def edit_playlist(request, playlist_id):
	return HttpResponse("")

def edit_record(request, record_id):
	return HttpResponse("")

def my_profile(request, user_id):
	user_profile = UserProfile.objects.get(id=user_id)

	t = loader.get_template("profile.html")
	c = RequestContext(request, {'user_profile': user_profile})
	return HttpResponse(t.render(c))
def library(request, list_type):
	user = get_user(request)
	
	LIST_HEADERS = (
				('Title', 'record__title'),
				('Artist', 'record__artist__name'),
				('Genre', 'record__genre__nane'),
				('Category', 'record__category__nane'),
				('# of Tracks', 'num_tracks'),
				('Producer', 'record__producer'),
				)
		
	sort_headers = SortHeaders(request, LIST_HEADERS) 
	records = RecordLibraryItem.objects.filter(user=user.id, \
											library__library_type=list_type)\
											.annotate(num_tracks=Count('record__recordtrack')).order_by(sort_headers.get_order_by())
	
	return object_list(request, template_name='library.html',
         queryset=records, paginate_by=10, extra_context={'list_type':list_type, 'headers': list(sort_headers.headers())})

@transaction.commit_on_success
def remove_from_library(request, ids):
	id_array = ids.split("_")
	for id in id_array:
		lib_item = RecordLibraryItem.objects.filter(user=get_user(request), record=Record(id=id))
		lib_item.delete()
	
	return HttpResponse()

def promote_tracked_to_owned(request, ids):
	id_array = ids.split("_")
	user = get_user(request)
	
	rec_lib = RecordLibrary.objects.get(user=user, library_type="O")
	for id in id_array:
		lib_item = RecordLibraryItem.objects.get(user=user, record=Record(id=id), library__library_type='T')
		lib_item.library = rec_lib
		lib_item.save()
	
	return HttpResponse()
	
@transaction.commit_on_success
def new_playlist(request, list_name, ids):
	cur_user = get_user(request)
	
	playlist = Playlist(created_by=cur_user, list_name=urllib.unquote(list_name), created_on=datetime.now())
	playlist.save()
		
	msg = save_to_playlist(cur_user, playlist, ids)
		
	return HttpResponse(msg)

@transaction.autocommit
def add_to_list(request, type, ids):
	
	id_array = ids.split("_")
	cur_user = get_user(request)
	
	rec_library = RecordLibrary.objects.filter(user=cur_user.id, library_type=type)
	if not(rec_library):
		rec_library = RecordLibrary(created_by=cur_user, library_type=type)
		rec_library.save()
	else:
		rec_library = rec_library[0]
	
	duplicate_ids = []
	inserted_recs = []
	for rec_id in id_array:
		try:
			item = RecordLibraryItem(library=rec_library, user=cur_user, record=Record(id=rec_id))
			item.save()
		except IntegrityError:
			duplicate_ids.append(item.record.id)
			transaction.rollback()
		else:
			inserted_recs.append(item.record.id)

	msg = ''
	if len(inserted_recs) > 0:
		id_inclause = 'id in (' + ",".join(inserted_recs) + ')'
		inserted_recs = Record.objects.extra(where=[id_inclause]).values('title')
		instd_rec_title = []
		for instd_rec in inserted_recs:
			instd_rec_title.append(instd_rec.get('title'))
		have = pluralize("have", len(inserted_recs))
		msg = ("'{0}' {1} been added. \n\n ".format("', '".join(instd_rec_title), have))
	if len(duplicate_ids) > 0:
		
		id_inclause = 'id in (' + ",".join(duplicate_ids) + ')'
		duplicate_recs = Record.objects.extra(where=[id_inclause]).values('title')
		dup_rec_title = []
		for dup_rec in duplicate_recs:
			dup_rec_title.append(dup_rec.get('title'))
		
		be = pluralize("be", len(duplicate_ids))
		msg += "'{0}' {1} already in the list.".format("', '".join(dup_rec_title), be)
		
	return HttpResponse(msg)

@transaction.commit_on_success
def add_to_playlist(request, playlist_id, ids):
	cur_user = get_user(request)
	msg = save_to_playlist(cur_user, Playlist(id=playlist_id), ids)		
	return HttpResponse(msg)

def save_to_playlist(cur_user, playlist, ids):
	id_array = ids.split("__")
	
	for id in id_array:
		trid = id.split("_")
		item = PlaylistItem(playlist=playlist, created_by=cur_user,
						track=Soundtrack(id=trid[0]), record=Record(id=trid[1]),
						)
		duplicate_ids = []
		inserted_ids = []
		try:
			item.save()
		except IntegrityError:
			duplicate_ids.append(trid[0])
			transaction.rollback()
		else:
			inserted_ids.append(trid[0])
	
	msg = ""
	if len(inserted_ids) > 0:
		id_inclause = 'id in (' + ",".join(inserted_ids) + ')'
		inserted_tracks = Soundtrack.objects.extra(where=[id_inclause]).values('title')
		instd_rec_title = []
		for instd_rec in inserted_tracks:
			instd_rec_title.append(instd_rec.get('title'))
			
		have = pluralize("have", len(inserted_tracks))
		msg = ("'{0}' {1} been added. \n\n ".format("', '".join(instd_rec_title), have))
	if len(duplicate_ids) > 0:
		
		id_inclause = 'id in (' + ",".join(duplicate_ids) + ')'
		duplicate_recs = Soundtrack.objects.extra(where=[id_inclause]).values('title')
		dup_rec_title = []
		for dup_rec in duplicate_recs:
			dup_rec_title.append(dup_rec.get('title'))
		
		be = pluralize("be", len(duplicate_ids) == 1)
		msg += "'{0}' {1} already in the list.".format("', '".join(dup_rec_title), be)
	return msg

def publish_playlist(request, playlist_id):
	msg = ''
	try:
		playlist = Playlist.objects.get(id=playlist_id, created_by=get_user(request))
		playlist.is_published = True
		playlist.published_on = datetime.now()
		playlist.save()
	except:
		msg = 'Could not publish the playlist'
	else:
		msg = 'The playlist has been published'
	return HttpResponse(msg)
		
def search_record(request):
	query_string = request.GET.get('q', '')
	cur_user = get_user(request)
	
	form = SearchForm()

	if query_string:
		LIST_HEADERS = (
				('Title', 'title'),
				('Matrix Number', 'matrix_number'),
				('Artists', 'artist__name'),
				('Rating', 'rating__avg_rating'),
				('Genre', 'genre__genre_name'),
				('Category', 'category__category_name'),
				)
		additional_params = 'q=' + query_string
		
		sort_headers = SortHeaders(request, LIST_HEADERS, additional_params={'q':query_string})

		entry_query = get_query(query_string.strip(), ['title', 'genre__genre_name', 'category__category_name',
													'artist__name', 'recordtrack__track__title', ])

		record_list = Record.objects.filter(entry_query).order_by(sort_headers.get_order_by())
		
		context = {'q':query_string, 'form': form, 'additional_params': additional_params, 'view': 'rec', 'headers': sort_headers.headers()}
		
		return object_list(request, template_name='search_results.html',
         queryset=record_list, paginate_by=10, extra_context=context) 
		
	else:
		form = SearchForm()
		context = {'form': form, 'record_list': []}
		
		t = loader.get_template("search_results.html")
		c = RequestContext(request, context)
		return HttpResponse(t.render(c))
		
#	return object_list(request, template_name='search_results.html',
#         queryset=record_list, paginate_by=2, extra_context = context)
		

def search_track(request):
	query_string = request.GET.get('q', '')
	cur_user = get_user(request) 
	
	playlists = Playlist.objects.filter(created_by=cur_user)
	
	form = SearchForm()

	if query_string:
		LIST_HEADERS = (
				('Title', 'track__title'),
				('Artists', 'track__trackartist__artist__name'),
				('Music Writer', 'track__music_writer'),
				('Release Date', 'track__release_date'),
				('Genre', 'track__genre__genre_name'),
				('Original Version', 'track__original_version__title'),
				)

		additional_params = 'q=' + query_string
		
		sort_headers = SortHeaders(request, LIST_HEADERS, additional_params={'q':query_string})

#		entry_query = get_query(query_string.strip(), ['title', 'genre__genre_name', 'music_writer', 
#													'trackartist__artist__name', 'recordtrack__record__title',])
#		track_list = Soundtrack.objects.select_related().filter(entry_query).order_by(sort_headers.get_order_by())

		entry_query = get_query(query_string.strip(), ['track__title', 'record__genre__genre_name',\
													'track__music_writer', 'track__genre__genre_name' ,\
													'track__trackartist__artist__name', 'record__title', ])
		track_list = Recordtrack.objects.filter(entry_query).order_by(sort_headers.get_order_by())
		
			
		context = {'q':query_string, 'form': form, 'additional_params': additional_params, \
				'playlists': playlists, 'view': 'track', 'headers': sort_headers.headers(), }
		
		
		return object_list(request, template_name='search_results.html',
         queryset=track_list, paginate_by=10, extra_context=context) 
				
	else:
		form = SearchForm()
		context = {'form': form, 'record_list': []}
		
		t = loader.get_template("search_results.html")
		c = RequestContext(request, context)
		return HttpResponse(t.render(c))
	
#def search(req):
#	return SearchView(template='search/search.html')(req)

def new_record(request):
	if request.method == 'POST':
		form = RecordForm(request.POST)
		if form.is_valid():
			record = form.save()
			logger.debug("testing register: if case")
#			return HttpResponseRedirect('/vinyl/record/' + str(record.id))
	else:
		form = RecordForm()
		
	return render_to_response('record/new_record.html', { 'form' : form }, context_instance=RequestContext(request))

def associate_track_to_record(request):
	import json
	if request.method == 'POST':
		form = RecordtrackForm(request.POST)
		record_id = request.POST["record"]
		if form.is_valid():
			recordtrack = form.save(commit=False)
			recordtrack.record_id = record_id
			recordtrack.disc_number = form.cleaned_data['disc_number']
			recordtrack.order = form.cleaned_data['order']
			if Recordtrack.objects.filter(record__id=record_id, track__id=recordtrack.track_id).count() > 0:
				return HttpResponse(json.dumps({"general_error":["This soundtrack is already associated with this Record"]}))
			recordtrack.save() 
			logger.debug("testing register: if case")
			return HttpResponse(json.dumps({"success": "true", "next" : "/vinyl/record/" + str(recordtrack.record_id)}))
		else:
			return HttpResponse(json.dumps(form.errors))
