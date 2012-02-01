from django.conf.urls.defaults import *
from adbproject.vinyl.views import playlists
from adbproject import settings


urlpatterns = patterns('', 
					#url(r'^$', 'vinyl.views.homepage', name='homepage'),
					url(r'^playlist.html*$', playlists),
						(r'^adbproject/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
                       
                )

