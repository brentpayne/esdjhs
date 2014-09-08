from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^<first_name>/$', views.first_name_search),
]
