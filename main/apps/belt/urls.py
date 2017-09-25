from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.register),
    url(r'^signIn$', views.signIn),
    url(r'^signOut$', views.signOut),
    url(r'^main$', views.main),
    url(r'^join/(?P<num>\d+)$', views.join),
    url(r'^add/(?P<num>\d+)$', views.add_trip),
    url(r'^create$', views.added),
    url(r'^destination/(?P<num>\d+)$', views.destination),
]
