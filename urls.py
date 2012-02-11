from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from adbproject.ajax_select import urls as ajax_select_urls

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	url(r'^$', 'vinyl.views.homepage', name='homepage'),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
	url(r'^accounts/logout/$', 'vinyl.views.logout_view'),
	url(r'^accounts/register/$', 'vinyl.views.register'),
    url(r'^search/', include('adbproject.vinyl.search-urls')),
#    (r'^search/', include('haystack.urls')),
#    url(r'^search/', include('adbproject.haystack_urls')),
	
	url(r'^test_view/$', 'vinyl.views.my_test_view'),
	
	url(r'^vinyl/', include('adbproject.vinyl.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/lookups/', include(ajax_select_urls)),
     url(r'^admin/', include(admin.site.urls)),
)