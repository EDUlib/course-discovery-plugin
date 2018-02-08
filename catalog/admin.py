# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.

from .models import Organisation

class OrganisationAdmin (admin.ModelAdmin):
    ordering = ('long_name',)

admin.site.register(Organisation, OrganisationAdmin)