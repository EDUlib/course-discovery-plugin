"""Code for the logic behind the catalogue html page."""
#-*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import locale
import requests
import dateutil.parser

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, Http404
from .models import Organisation

locale.setlocale(locale.LC_ALL, 'fr_CA')

# Create your views here.

def catalog(request):
    """Code for the catalog html page."""
    #Initial setup
    auth = (settings.EDULIB_USER, settings.EDULIB_PWD)
    answer = requests.get(settings.EDULIB_DISCO, auth=auth)
    data = json.loads(answer.text)
    course_upcoming = []
    course_current = []
    course_past = []

    #Prepare content of the index
    for each in data['results']:
        run = each['course_runs']
        if run != []:
            owner = each['owners']
            owner_key = owner[0]['key']
            #Check if org_url is valid
            #Skip the content preparation if associated organisation doesnt exist or cannot be shown
            try:
                org = Organisation.objects.get(short_name = owner_key.lower(), show_org = True)
                convert_owner(run, org)
            except:
                continue
            
            convert_course(run, owner_key)
            convert_time(run)
            categorize(run, course_upcoming, course_current, course_past)

    #Values passed to html
    context = {
        'course_upcoming': course_upcoming,
        'course_current': course_current,
        'course_past': course_past,
        'EDULIB_LMS': settings.EDULIB_LMS,
        'EDULIB_CATALOG': settings.EDULIB_CATALOG,
    }
    return render(request, 'catalog/index.html', context)

def organisation(request, org_name):
    """Code for the organisations' html page."""
    #Check if org_name is valid
    #Raise error 404 if requested organisation doesnt exist or cannot be shown
    org_obj = get_object_or_404(Organisation, short_name = org_name.lower(), show_org = True)
    
    #Initial setup
    auth = (settings.EDULIB_USER, settings.EDULIB_PWD)
    answer = requests.get(settings.EDULIB_DISCO, auth=auth)
    data = json.loads(answer.text)
    course_upcoming = []
    course_current = []
    course_past = []

    #Prepare content of the index
    for each in data['results']:
        run = each['course_runs']
        if run != []:
            owner = each['owners']
            owner_key = owner[0]['key']
            if owner_key.lower() == org_name.lower():
                convert_owner(run, org_obj)
                convert_course(run, owner_key)
                convert_time(run)
                categorize(run, course_upcoming, course_current, course_past)
    
    #Values passed to html
    context = {
        'course_upcoming': course_upcoming,
        'course_current': course_current,
        'course_past': course_past,
        'EDULIB_LMS': settings.EDULIB_LMS,
        'EDULIB_CATALOG': settings.EDULIB_CATALOG,
        'ORG_MODEL': org_obj,
    }
    return render(request, 'catalog/org_index.html', context)

def convert_time(run):
    """Convert the timecode into a nice localized string for a nice print."""
    if run[0]['end']:
        yourdate_end = dateutil.parser.parse(run[0]['end'])
        run[0]['end_print'] = yourdate_end.strftime("%d %B %Y")
    if run[0]['start']:
        yourdate_start = dateutil.parser.parse(run[0]['start'])
        run[0]['start_print'] = yourdate_start.strftime("%d %B %Y")
    return run

def categorize(run, course_upcoming, course_current, course_past):
    """Separate course using their availability status."""
    if (run[0]['availability'] in ('Upcoming', 'Starting Soon') and not run[0]['hidden']):
        course_upcoming.append(run[0])
    elif run[0]['availability'] == 'Current' and not run[0]['hidden']:
        course_current.append(run[0])
    elif run[0]['availability'] == 'Archived' and not run[0]['hidden']:
        course_past.append(run[0])
    else:
        pass
    return course_upcoming, course_current, course_past

def convert_owner(run, owner):
    """Swap the owner key for the long name for a nice print"""
    owner_print=owner.long_name
    run[0]['owner_print'] = owner_print
    return run

def convert_course(run, owner_key):
    """Truncate the owner key from the course key string for a nice print."""
    key = run[0]['course']
    run[0]['course_print'] = key[len(owner_key)+1:]
    return run
    