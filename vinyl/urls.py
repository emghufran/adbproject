from django.conf.urls.defaults import *
from adbproject.vinyl.views import *
from adbproject import settings


urlpatterns = patterns('', 
					#url(r'^$', 'vinyl.views.homepage', name='homepage'),
					url(r'^lang/(?P<lang>\w+)$', change_language),	
                    
                    url(r'track/new/(?P<record_id>\d+)/$', new_track, name='new_track_url'),
                    url(r'^track/(?P<track_id>\d+)$', track_details),
                    url(r'^track/edit/(?P<track_id>\d+)/$', edit_track, name='edit_track_url'),
                    url(r'^track/delete/(?P<track_id>\d+)/(?P<record_id>\d+)/$', delete_track, name='delete_track_url'),
                    
					url(r'^playlists/(?P<pltype>\w+)$', playlists),
                    url(r'^playlist/(?P<playlist_id>\d+)$', playlist_details),
                    url(r'^playlist/edit/(?P<playlist_id>\d+)$', edit_playlist),
                    url(r'^playlist/add/(?P<playlist_id>\d+)/(?P<ids>\w+)$', add_to_playlist),
                    url(r'^playlist/new/(?P<list_name>\w+)/(?P<ids>\w+)$', new_playlist),
                    url(r'^playlist/publish/(?P<playlist_id>\d+)$', publish_playlist),
                    
                    url(r'^list/add/(?P<type>\w)/(?P<ids>\w+)$', add_to_list),

                    url(r'^record/(?P<record_id>\d+)$', record_details),  
                    url(r'^record/new/$', new_record),
                    url(r'^record/edit/(?P<record_id>\d+)/$', edit_record, name='edit_record_url'),
                    url(r'^record/associate_track_to_record/$', associate_track_to_record),

					url(r'^library/(?P<list_type>\w)/$', library), 
					url(r'^library/delete/(?P<ids>\w+)/$', remove_from_library),
					url(r'^library/promote/(?P<ids>\w+)/$', promote_tracked_to_owned),
					
                )
