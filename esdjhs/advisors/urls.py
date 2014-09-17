from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<first_name>\S+)/$', views.first_name_search),
]
