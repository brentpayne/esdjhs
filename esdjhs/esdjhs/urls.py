from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^search/', include('haystack.urls')),
    (r'^advisors/', include('advisors.urls')),  # new line
    url(r'^admin/', include(admin.site.urls)),
)
