from adbproject import settings
from adbproject.vinyl.models import Rating, Record, Playlist
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.utils.translation import activate
from django.views.generic.list_detail import object_list


from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from adbproject.vinyl.models import UserProfileForm

def homepage(request):
	from django.db.models import Q

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
	from django.db.models import Q
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
		form = UserCreationForm(request.POST)
		profile_form = UserProfileForm(request.POST)
	else:
		form = UserCreationForm()
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
  	tracks = record.recordtrack_set.all()
  	comments = record.comment_set.all()
  	
#  	rating = Rating.objects.get(record=record_id) 
  	
  	t = loader.get_template("record_details.html")
  	c = RequestContext(request, {'record': record, 'rating':rating, 'comments': comments, 'tracks': tracks })
  	return HttpResponse(t.render(c))
