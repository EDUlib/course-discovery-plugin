# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here
app_name = 'catalog'
class Organisation(models.Model):
    short_name  = models.CharField(max_length=50,unique=True)
    long_name   = models.CharField(max_length=100)
    logo        = models.CharField(max_length=1000)
    org_url     = models.CharField(max_length=1000, verbose_name="URL")
    description = models.TextField()
    show_org    = models.BooleanField(default=True, verbose_name="Show organisation in index")
    
    def __str__(self):
        return self.long_name
