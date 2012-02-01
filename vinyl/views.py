from django.template import loader, Context
from django.http import HttpResponse
from django.utils.translation import activate
from django.http import HttpRequest
from adbproject import settings

def playlists(request):
    language = request.GET.get('lang', settings.LANGUAGE_CODE)
    
    activate(language)
    t = loader.get_template("playlists.html")
    c = Context({})
    response = HttpResponse(t.render(c))
    response.set_cookie('lang', language)
    return response