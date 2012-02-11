from django.conf.urls.defaults import *
from adbproject.vinyl.views import search_record, search_track
from adbproject import settings


urlpatterns = patterns('', 
                       url(r'^$', search_record),
                       url(r'^track/$', search_track),
                       )
