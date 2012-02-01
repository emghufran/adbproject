from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.utils.translation import activate
from django.http import HttpRequest
from adbproject import settings

from django.shortcuts import render_to_response
def homepage(request):
	t = loader.get_template('base.html')
	c = RequestContext( request, { 
		'latest_poll_list': 'abcd', 'content' : "hahahaha", 'page_title' : 'test title'
	})
	return HttpResponse(t.render(c))
	#return render_to_response('base.html', {'latest_poll_list': 'abcd'})
	
def playlists(request):
    language = request.GET.get('lang', settings.LANGUAGE_CODE)
    
    activate(language)
    t = loader.get_template("playlists.html")
    c = Context({})
    response = HttpResponse(t.render(c))
    response.set_cookie('lang', language)
    return response