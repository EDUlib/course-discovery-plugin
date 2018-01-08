from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url('catalog/', include('catalog.urls')),
    url('admin/', admin.site.urls),
]
