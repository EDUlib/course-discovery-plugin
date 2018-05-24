from django.conf.urls import url

from . import views

app_name = 'catalog'
urlpatterns = [
    url(r'^$', views.catalog_fr, name='catalog_fr'),
    url(r'^fr/$', views.catalog_fr, name='catalog_fr'),
    url(r'^en/$', views.catalog_en, name='catalog_en'),
    url(r'^en/(?P<org_name>[a-zA-Z0-9]+)/$', views.organisation_en, name='organisation_en'),
    url(r'^(?P<org_name>[a-zA-Z0-9]+)/$', views.organisation_fr, name='organisation_fr'),   
]
