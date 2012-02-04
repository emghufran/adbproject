from adbproject import settings
from adbproject.vinyl.models import Record
from adbproject.vinyl.models import Rating
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.utils.translation import activate
from django.views.generic.list_detail import object_list

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
	
def playlists(request):
    t = loader.get_template("playlists.html")
    c = RequestContext(request, {})
    response = HttpResponse(t.render(c))
    return response
	

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

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
