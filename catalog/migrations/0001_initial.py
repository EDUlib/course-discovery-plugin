# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-11 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ecoles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_court', models.CharField(max_length=50)),
                ('nom_long', models.CharField(max_length=100)),
                ('logo', models.CharField(max_length=1000)),
            ],
        ),
    ]