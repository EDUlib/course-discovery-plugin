# -*- coding: utf-8 -*-

from django.conf import settings

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import requests ;
import json ;

from pprint import pprint ;

from datetime import datetime ;
from operator import itemgetter ;
from django.template import loader ;

import timestring ;
import dateutil.parser;
import time;
import locale;

from .models import Ecoles

##### this could be set in the settings?
locale.setlocale(locale.LC_ALL, 'fr_CA')




def institution(request, school):

    ##### translating school to all lower case
    school = school.lower()


    ##### depending on school, switching to real name used in Course Discovery
    if school == 'polymtl':
       school = 'PolyMtl'
    elif school == 'umontreal':
       school = 'UMontreal'
    elif school == 'hec':
       school = 'HEC'
    else:
       school = 'unknown'


    ##### get courses from course discovery
    all_courses = requests.get(settings.EDULIB_DISCO, auth=(settings.EDULIB_USER, settings.EDULIB_PWD)) ;


    ##### transforming all courses in a single JSON structure
    json_data  = all_courses.json()


    ##### pretty print of all courses
    json_pretty_poly  = json.dumps(json_data,  sort_keys=True, indent=4)


    ##### getting "results" record
    results = json_data.get('results')


    ##### getting current date in ISO format
    current = datetime.now().isoformat()


    ##### getting list of courses in "results"
    mylist = []
    for course in results:
       if course['course_runs']:
          mylist.append(course)

    ##### filtering course_runs based on specific school
    mylist2 = []
    for course in mylist:
       if course['owners']:
          owners = course['owners']
          course_run = course['course_runs']
          if school in owners[0]['key']:
             if course_run[0]['end']:
                yourdate_end = dateutil.parser.parse(course_run[0]['end'])
                course_run[0]['end_affiche'] = yourdate_end.strftime("%d %B %Y")
             if course_run[0]['start']:
                yourdate_start = dateutil.parser.parse(course_run[0]['start'])
                course_run[0]['start_affiche'] = yourdate_start.strftime("%d %B %Y")
             mylist2.append(course)


    ##### extracting course runs
    mylist3 = []
    for course in mylist2:
       if course['course_runs']:
          course_run  = course['course_runs']
          mylist3.append(course_run)


    ##### calculating number of course runs
    long3 = len(mylist3)


    ##### extracting first element of all courses
    mylist4 = []
    i = 0
    while i < long3:
       y = mylist3[i][0]
       mylist4.append(y)
       i = i + 1


    #####  3 arrays for upcoming, current, done courses
    upcoming = []
    current  = []
    done     = []
    liste_totale = []


    ##### populate all 3 arrays based on criteria
    for cours in mylist4:
        if cours['availability'] == "Upcoming" and not cours['hidden']:
           upcoming.append(cours)
        elif cours['availability'] == "Current" and not cours['hidden']:
             current.append(cours)
        elif cours['availability'] == "Archived":
             done.append(cours)


    ##### sort arrays based on EDUlib chosen order
    upcoming_by_start = sorted(upcoming, key=itemgetter('start'), reverse=True)
    current_by_start  = sorted(current, key=itemgetter('start'), reverse=True)
    done_by_start     = sorted(done, key=itemgetter('end'), reverse=True)


    ##### add all 3 arrays to global context
    liste_totale.append(upcoming_by_start)
    liste_totale.append(current_by_start)
    liste_totale.append(done_by_start)


    ##### add school to global context
    ecole = ""
    if school is 'PolyMtl':
       ecole = "Polytechnique"
    elif school is 'UMontreal':
       ecole = "Université de Montréal"
    elif school is 'HEC':
       ecole = "Hautes Etudes Commerciales"
    liste_totale.append(ecole)


    ##### initialize global context
    context = {'cours_non_finis': liste_totale, 'edulib_lms': settings.EDULIB_LMS}


    ##### setting up template name
    if school is 'PolyMtl':
       school = "polymtl"
    elif school is 'UMontreal':
       school = "umontreal"
    elif school is 'HEC':
       school = "hec"
    template = 'catalog/' + school + '.html'


    ##### affichage du contexte via le template de l'institution
    return render(request, template, context)





def index(request):

    ##### get courses from course discovery
    all_courses = requests.get(settings.EDULIB_DISCO, auth=(settings.EDULIB_USER, settings.EDULIB_PWD)) ;


    ##### transforming all courses in a single JSON structure
    json_data  = all_courses.json()


    ##### pretty print of all courses
    json_pretty_poly  = json.dumps(json_data,  sort_keys=True, indent=4)


    ##### getting "results" record
    results = json_data.get('results')


    ##### getting current date in ISO format
    current = datetime.now().isoformat()


    ##### extracting courses from course_runs and sorting according to course state
    mylist = []
    for course in results:
       if course['course_runs']:
          course_run = course['course_runs']
          if course_run[0]['start']:
             if course_run[0]['end']:
                if ((course_run[0]['start'] < current and course_run[0]['end'] > current) or (course_run[0]['start'] > current)) and (course_run[0]['availability'] == "Current" or course_run[0]['availability'] == "Upcoming"):
                    mylist.append(course_run)
             else:
                if (course_run[0]['start'] > current) and (course_run[0]['availability'] == "Current" or course_run[0]['availability'] == "Upcoming"):
                   mylist.append(course_run)
          

    ##### converting ISO date in format more suitable for displaying the date
    ##### adding 2 new fields: start_affiche and end_affiche to current course_run
    mylist2 = mylist
    mylist3 = []
    long = len(mylist2)
    i = 0
    while i < long:
       course_run = mylist2[i]
       if course_run[0]['end']:
          yourdate_end = dateutil.parser.parse(course_run[0]['end'])
          course_run[0]['end_affiche'] = yourdate_end.strftime("%d %B %Y")
       if course_run[0]['start']:
          yourdate_start = dateutil.parser.parse(course_run[0]['start'])
          course_run[0]['start_affiche'] = yourdate_start.strftime("%d %B %Y")
       mylist3.append(course_run[0])
       i = i + 1 


    ##### sorting according to EDUlib sort order 
    mylist3_by_end = sorted(mylist3, key=itemgetter('start'), reverse=True)


    ##### setup global context
    all_ecoles = Ecoles.objects.all()
    context = {'cours_non_finis': mylist3_by_end, 'edulib_lms': settings.EDULIB_LMS, 'edulib_catalog': settings.EDULIB_CATALOG, 'all_ecoles': all_ecoles}


    ##### rendering page (can catalog/index.html be a settings?)
    return render(request, 'catalog/index.html', context)
