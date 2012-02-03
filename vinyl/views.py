from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.utils.translation import activate
from django.http import HttpRequest, HttpResponseRedirect
from adbproject import settings

from django.shortcuts import render_to_response
def homepage(request):
	t = loader.get_template('base.html')
	c = RequestContext(request, {})
	return HttpResponse(t.render(c))
	#return render_to_response('base.html', {'latest_poll_list': 'abcd'})
	
def playlists(request):
    t = loader.get_template("playlists.html")
    c = RequestContext(request, {})
    response = HttpResponse(t.render(c))
    return response
	
from django.contrib.auth import logout

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def change_language(request, lang):
    activate(lang)
    response = HttpResponse()
    response.set_cookie('django_language', lang)
    response.write(True)
    return response
