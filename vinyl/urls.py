from django.conf.urls.defaults import *
from adbproject.vinyl.views import *
from adbproject import settings


urlpatterns = patterns('', 
					#url(r'^$', 'vinyl.views.homepage', name='homepage'),
					url(r'^playlists/(?P<pltype>\w+)$', playlists),
					url(r'^lang/(?P<lang>\w+)$', change_language),	
                    url(r'^record/(?P<record_id>\d+)$', record_details),  
                    url(r'^playlist/(?P<playlist_id>\d+)$', playlist_details),
                    url(r'^track/(?P<track_id>\d+)$', track_details),
                    url(r'^track/edit/(?P<track_id>\d+)$', edit_track),
                    url(r'^playlist/edit/(?P<playlist_id>\d+)$', edit_playlist),
                    url(r'^record/edit/(?P<record_id>\d+)$', edit_record)
                )
