from django.conf.urls import url

from . import views

app_name = 'catalog'
urlpatterns = [
    url(r'^$', views.catalog, name='catalog'),
    #url(r'^hec/$', views.hec, name='hec'),
    #url(r'^polymtl/$', views.polymtl, name='polymtl'),
    #url(r'^umontreal/$', views.umontreal, name='umontreal'),
    url(r'^(?P<org>[a-zA-Z0-9]+)/$', views.organisation, name='organisation'),
]
