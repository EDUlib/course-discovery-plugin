# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here

class Ecoles(models.Model):
    nom_court = models.CharField(max_length=50)
    nom_long  = models.CharField(max_length=100)
    logo      = models.CharField(max_length=1000)

