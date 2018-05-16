from django.conf.urls import url

from . import views

app_name = 'catalog'
urlpatterns = [
    url(r'^$', views.catalog, name='catalog'),
    url(r'^en/$', views.catalog, name='catalog_en'),
    url(r'^en/(?P<org_name>[a-zA-Z0-9]+)/$', views.organisation, name='organisation_en'),
    url(r'^(?P<org_name>[a-zA-Z0-9]+)/$', views.organisation, name='organisation'),   
]
