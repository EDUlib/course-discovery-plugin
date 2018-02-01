"""Code for the logic behind the catalogue html page."""
#-*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import locale
import requests
import dateutil.parser

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.http import Http404

locale.setlocale(locale.LC_ALL, 'fr_CA')

# Create your views here.

def catalog(request):
    """Code for the index html page."""

    auth = (settings.EDULIB_USER, settings.EDULIB_PWD)
    answer = requests.get(settings.EDULIB_DISCO, auth=auth)
    data = json.loads(answer.text)
    course_upcoming = []
    course_current = []
    course_past = []

    for each in data['results']:
        run = each['course_runs']
        if run != []:
            owner = each['owners']
            owner_key = owner[0]['key']
            convert_owner(run, owner_key)
            convert_course(run, owner_key)
            convert_time(run)
            categorize(run, course_upcoming, course_current, course_past)

    context = {
        'course_upcoming': course_upcoming,
        'course_current': course_current,
        'course_past': course_past,
        'EDULIB_LMS': settings.EDULIB_LMS,
    }
    return render(request, 'catalog/index.html', context)
    #return HttpResponse(data['results'])

def organisation(request, org):
    """Code for the organisations' html page."""

    auth = (settings.EDULIB_USER, settings.EDULIB_PWD)
    answer = requests.get(settings.EDULIB_DISCO, auth=auth)
    data = json.loads(answer.text)
    course_upcoming = []
    course_current = []
    course_past = []

    for each in data['results']:
        run = each['course_runs']
        if run != []:
            owner = each['owners']
            owner_key = owner[0]['key']
            if owner_key.lower() == org.lower():
                convert_owner(run, owner_key)
                convert_course(run, owner_key)
                convert_time(run)
                categorize(run, course_upcoming, course_current, course_past)

    if (not course_upcoming and not course_current and not course_past):
        raise Http404('Theres is no institution named '+ org)

    context = {
        'course_upcoming': course_upcoming,
        'course_current': course_current,
        'course_past': course_past,
        'EDULIB_LMS': settings.EDULIB_LMS,
    }
    return render(request, 'catalog/umontreal.html', context)
    #return HttpResponse(course_past)

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

def convert_course(run, owner_key):
    """Truncate the owner key from the course key string for a nice print."""

    key = run[0]['course']
    run[0]['course_print'] = key[len(owner_key)+1:]
    return run

def convert_owner(run, owner):
    """Swap the owner key for the long name for a nice print and hide unsupported organisations"""

    owner_print = owner
    if owner.lower() == 'umontreal':
        owner_print = "Université de Montréal"
    elif owner.lower() == 'polymtl':
        owner_print = "Polytechnique Montréal"
    elif owner.lower() == 'hec':
        owner_print = "HEC Montréal"
    else:
        run[0]['hidden'] = True
    run[0]['owner_print'] = owner_print
    return run
