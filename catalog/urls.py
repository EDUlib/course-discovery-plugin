from django.conf.urls import url

from . import views

urlpatterns = [
    url('(?P<school>[a-zA-Z0-9]+)', views.institution),
    url('', views.index, name='index'),
]
