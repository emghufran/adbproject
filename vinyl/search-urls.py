from django.conf.urls.defaults import *
from adbproject.vinyl.views import library,search_record
from adbproject import settings


urlpatterns = patterns('', 
                       
                       url(r'^$', search_record)
                       )
