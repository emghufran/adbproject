from adbproject import settings
from adbproject.vinyl.forms import *
from adbproject.vinyl.models import *
from adbproject.vinyl.snippets.tablesorter import SortHeaders
from django.contrib.auth import logout, logout, logout, get_user
from django.contrib.auth.forms import UserCreationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail, send_mail
from django.core.paginator import Paginator
from django.db.models.aggregates import Count
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.utils.translation import activate
from django.views.generic.list_detail import object_list
from haystack.views import SearchView
import datetime
import logging



logger = logging.getLogger('django.request')

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
	curuser = get_user(request)
	user = User.objects.get(id=curuser.id)
	
	LIST_HEADERS = (
				('Playlist', 'list_name'),
				('Created by', 'created_by__username'),
				('Created on', 'created_on'),
				('# of Records', 'num_records'),
				)
		
	sort_headers = SortHeaders(request, LIST_HEADERS)
	if (pltype == 'my'):
		playlists = Playlist.objects.filter(created_by__id=user.id).annotate(num_records=Count('playlistitem')).order_by(sort_headers.get_order_by())
#		playlists = user.playlist_set.all()
	elif (pltype == 'sharedwm'):
		playlists = Playlist.objects.filter(playlistshare__shared_to__id=user.id).annotate(num_records=Count('playlistitem')).order_by(sort_headers.get_order_by())
#		playlists = user.shared_user.all()
	elif (pltype == 'myshared'):
		playlists = Playlist.objects.filter(playlistshare__created_by__id=user.id).annotate(num_records=Count('playlistitem')).order_by(sort_headers.get_order_by())
#		playlists = user.owner.all()
	else:
		pltype = 'all'
		playlists = Playlist.objects.annotate(num_records=Count('playlistitem')).order_by(sort_headers.get_order_by())
		
#    users = User.objects.order_by(sort_headers.get_order_by())
#    return render_to_response('users/user_list.html', {
#        'users': users,
#        'headers': list(sort_headers.headers()),
#    })
	
	return object_list(request, template_name = 'playlists.html',
         queryset = playlists, paginate_by = 10, extra_context={'ptype':pltype,'headers': list(sort_headers.headers())})
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
	c = RequestContext(request, {'record': record, 'rating':rating, 'comments': comments, 'data': data, 'recordtracks': recordtracks, 'artists': artists, 'recordtrack_form' : recordtrack_form})
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
def new_track(request, record_id=None):
	return HttpResponse("")

def edit_playlist(request, playlist_id):
	return HttpResponse("")

def edit_record(request, record_id):
	return HttpResponse("")

def library(request):
	return HttpResponse("s")

def add_to_list(request, type, ids):
	
	id_array = ids.split("_")
	cur_user = get_user(request)
	
	rec_library = RecordLibrary.objects.filter(user=cur_user.id, library_type=type)
	if not(rec_library):
		rec_library = RecordLibrary(user=cur_user, library_type=type)
		rec_library.save()
		print "Reclib saved"
	else:
		rec_library = rec_library[0]
	
	
#	lib_id = rec_library.id
	cur_time = datetime.time()
	print cur_time
	
	for rec_id in id_array:
		print rec_id
		print rec_library
		item = RecordLibraryItem(library=rec_library, user=cur_user, record=Record(id=rec_id))
		item.save()
		
	return HttpResponse("")

def search_record(request):
	query_string = request.GET.get('q','')
	cur_user = get_user(request)
	
	playlists = Playlist.objects.filter(created_by__id=cur_user.id)
	
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
		additional_params = 'q='+query_string
		
		sort_headers = SortHeaders(request, LIST_HEADERS, additional_params={'q':query_string})

		entry_query = get_query(query_string.strip(), ['title', 'genre__genre_name', 'category__category_name', 
													'artist__name', 'recordtrack__track__title',])
		print entry_query
		record_list = Record.objects.filter(entry_query).order_by(sort_headers.get_order_by())
##		entry_query = get_query(query_string.strip(), ['record__title', 'record__genre__genre_name', 'record__category__category_name', 'record__artist__name',
##													'track__title', 'track__trackartist__artist__name'])
#		entry_query = get_query(query_string.strip(), ['record__title', 'record__genre__genre_name', 'record__artist__name',
#													'track__title', ])
#		print entry_query
#		record_list= Recordtrack.objects.filter(entry_query)
		print record_list.count()
		
		context = {'q':query_string, 'form': form, 'additional_params': additional_params, 'playlists': playlists, 'view': 'rec', 'headers': sort_headers.headers()}
		
		return object_list(request, template_name='search_results.html',
         queryset=record_list, paginate_by=10, extra_context = context) 
		
#	if ('q' in request.GET) and request.GET['q'].strip():
#		query_string = request.GET['q']
#		
#		entry_query = get_query(query_string, ['title', ])
#		
#		record_list = Record.objects.filter(entry_query)
#		
#		context = {'q':query_string}
		
	else:
		form = SearchForm()
		context = {'form': form, 'record_list': []}
		
		t = loader.get_template("search_results.html")
		c = RequestContext(request, context)
		return HttpResponse(t.render(c))
		
#	return object_list(request, template_name='search_results.html',
#         queryset=record_list, paginate_by=2, extra_context = context)
		

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
		if form.is_valid():
			recordtrack = form.save(commit=False)
			recordtrack.record_id = request.POST["record"]
			recordtrack.disc_number = form.cleaned_data['disc_number']
			recordtrack.order = form.cleaned_data['order']
			
			recordtrack.save() 
			logger.debug("testing register: if case")
			return HttpResponse(json.dumps({"success": "true", "next" : "/vinyl/record/" + str(recordtrack.record_id)}))
		else:
			return HttpResponse(json.dumps(form.errors))

def json_response(x):
	import json
	return HttpResponse(json.dumps(x, sort_keys=True, indent=2), content_type='application/json; charset=UTF-8')
