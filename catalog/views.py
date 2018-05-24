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
from .models import Organisation, CourseURL

#locale.setlocale(locale.LC_ALL, settings.LANGUAGE_CODE)

# Create your views here.
def catalog_fr(request):
    return catalog(request, 'fr_CA', 'catalog/index.html')

def catalog_en(request):
    return catalog(request, 'en_US', 'catalog/index_en.html')

def organisation_fr(request, org_name):
    return organisation(request, org_name, 'fr_CA', 'catalog/org_index.html')

def organisation_en(request, org_name):
    return organisation(request, org_name, 'en_US', 'catalog/org_index_en.html')

def catalog(request, lang, index):
    """Code for the catalog html page."""
    #Initial setup
    locale.setlocale(locale.LC_ALL, lang)
    auth = (settings.EDULIB_USER, settings.EDULIB_PWD)
    search = (settings.EDULIB_DISCO+settings.EDULIB_DISCO_SEARCH)
    answer = requests.get(search, auth=auth)
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
                org_obj = Organisation.objects.get(short_name = owner_key.lower(), show_org = True)
            except:
                continue
            convert_owner(run, org_obj)
            convert_course(run, owner_key)
            convert_time(run)
            convert_url(run)
            convert_image(each)
            categorize(run, course_upcoming, course_current, course_past)
            

    #Values passed to html
    context = {
        'course_upcoming': course_upcoming,
        'course_current': course_current,
        'course_past': course_past,
        'EDULIB_LMS': settings.EDULIB_LMS,
        'EDULIB_DISCO': settings.EDULIB_DISCO,
        'organisation': Organisation.objects.filter(show_org=True).order_by('long_name'),
    }
    return render(request, index, context)

def organisation(request, org_name, lang, index):
    """Code for the organisations' html page."""
    #Check if org_name is valid
    #Raise error 404 if requested organisation doesnt exist or cannot be shown
    locale.setlocale(locale.LC_ALL, lang)
    try:
        org_obj = Organisation.objects.get(short_name = org_name.lower())
    except:
        return render(request, 'catalog/unknown.html')
    
    #Initial setup
    auth = (settings.EDULIB_USER, settings.EDULIB_PWD)
    search = (settings.EDULIB_DISCO+settings.EDULIB_DISCO_SEARCH)
    answer = requests.get(search, auth=auth)
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
                convert_url(run)
                convert_image(each)
                categorize(run, course_upcoming, course_current, course_past)
    
    header = "catalog/header_no.html"
    if org_obj.show_org and lang=='fr_CA':
        header = "catalog/header.html"
    elif org_obj.show_org and lang=='en_US':
        header = "catalog/header_en.html"

    #Values passed to html
    context = {
        'course_upcoming': course_upcoming,
        'course_current': course_current,
        'course_past': course_past,
        'EDULIB_LMS': settings.EDULIB_LMS,
        'EDULIB_DISCO': settings.EDULIB_DISCO,
        'ORG_MODEL': org_obj,
        'organisation': Organisation.objects.filter(show_org=True).order_by('long_name'),
        'header': header,
    }
    return render(request, index, context)

def convert_time(run):
    """Convert the timecode into a nice localized string for a nice print."""
    if run[0]['end']:
        yourdate_end = dateutil.parser.parse(run[0]['end'])
        run[0]['end_print'] = yourdate_end.strftime("%d %B %Y")
    if run[0]['start']:
        yourdate_start = dateutil.parser.parse(run[0]['start'])
        run[0]['start_print'] = yourdate_start.strftime("%d %B %Y")

def categorize(run, course_upcoming, course_current, course_past):
    """Separate course using their availability status."""
    if run[0]['availability'] in ('Upcoming', 'Starting Soon') and not run[0]['hidden']:
        course_upcoming.append(run[0])
    elif run[0]['availability'] == 'Current' and not run[0]['hidden']:
        course_current.append(run[0])
    elif run[0]['availability'] == 'Archived' and not run[0]['hidden']:
        course_past.append(run[0])
    else:
        pass

def convert_owner(run, owner):
    """Swap the owner key for the long name for a nice print"""
    owner_print=owner.long_name
    run[0]['owner_print'] = owner_print

def convert_course(run, owner_key):
    """Truncate the owner key from the course key string for a nice print."""
    key = run[0]['course']
    run[0]['course_print'] = key[len(owner_key)+1:]

def convert_url (run):
    """Check if url has to be changed, use default url if course_key is not in table"""
    key = run[0]['key']
    try:
        courseURL_obj = CourseURL.objects.get(course_key = key)
        run[0]['courseURL'] = courseURL_obj.url
    except:
        run[0]['courseURL'] = settings.EDULIB_LMS + ('/courses/') + key +('/about')

def convert_image (course):
    """If course_run image is empty, use the course image"""
    if course['course_runs'][0]['image']:
        course['course_runs'][0]['image_src']=course['course_runs'][0]['image']['src']
    else:
        course['course_runs'][0]['image_src']=settings.EDULIB_DISCO+course['original_image']['src']