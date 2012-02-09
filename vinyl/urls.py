from django.conf.urls.defaults import * 
from adbproject.vinyl.views import *
from adbproject import settings


urlpatterns = patterns('', 
					#url(r'^$', 'vinyl.views.homepage', name='homepage'),
					url(r'^playlists/(?P<pltype>\w+)$', playlists),
					url(r'^lang/(?P<lang>\w+)$', change_language),	
                    url(r'^record/(?P<record_id>\d+)$', record_details),  
                    url(r'^playlist/(?P<playlist_id>\d+)$', playlist_details),
                    
                    url(r'^track/new/(?P<record_id>\d+)/$', new_track),
                    url(r'^track/(?P<track_id>\d+)$', track_details),
                    url(r'^track/edit/(?P<track_id>\d+)$', edit_track),
                    url(r'^playlist/edit/(?P<playlist_id>\d+)$', edit_playlist),
                    
                    url(r'^list/add/(?P<type>\w)/(?P<ids>\w+)$', add_to_list),
                    url(r'^record/new/$', new_record),
                    url(r'^record/edit/(?P<record_id>\d+)$', edit_record),

					url(r'^library/$', library), 
                    url(r'^record/associate_track_to_record/$', associate_track_to_record),
                )