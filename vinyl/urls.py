from django.conf.urls.defaults import *
from adbproject.vinyl.views import *
from adbproject import settings


urlpatterns = patterns('', 
					#url(r'^$', 'vinyl.views.homepage', name='homepage'),
					url(r'^playlist*$', playlists),
					url(r'^lang/(?P<lang>\w+)$', change_language),	
                    url(r'^record/(?P<record_id>\d+)$', record_details)  
                )
