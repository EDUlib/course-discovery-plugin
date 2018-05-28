from django.conf.urls import url
from django.views.generic import RedirectView
from . import views


app_name = 'catalog'
urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/home/fr', permanent=False)),
    url(r'^home/en$', views.catalog_en, name='catalog_en'),
    url(r'^home/fr$', views.catalog_fr, name='catalog_fr'),
    url(r'^home$', RedirectView.as_view(url='/home/fr', permanent=False)),
    url(r'^(?P<org_name>[a-zA-Z0-9]+)/en$', views.organisation_en, name='organisation_en'),
    url(r'^(?P<org_name>[a-zA-Z0-9]+)/fr$', views.organisation_fr, name='organisation_fr'),
    url(r'^(?P<org_name>[a-zA-Z0-9]+)/$', views.organisation_fr, name='organisation_fr'),
]
