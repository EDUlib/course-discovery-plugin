from django.conf.urls import url

from . import views

app_name = 'catalog'
urlpatterns = [
    url(r'^$', views.catalog, name='catalog'),
    url(r'^(?P<org_name>[a-zA-Z0-9]+)/$', views.organisation, name='organisation'),
]
