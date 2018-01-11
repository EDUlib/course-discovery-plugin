from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('(?P<school>[a-zA-Z0-9]+)', views.institution),
    url('', views.index, name='index'),
]
