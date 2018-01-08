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

locale.setlocale(locale.LC_ALL, 'fr_CA')




def institution(request, school):

    #####print school
    #####print school.lower()
    school = school.lower()

    ##### institution en minuscule, je ramene dans le nom dans Course Discovery #####
    if school == 'polymtl':
       school = 'PolyMtl'
    elif school == 'umontreal':
       school = 'UMontreal'
    elif school == 'hec':
       school = 'HEC'
    else:
       school = 'unknown'

    #####print school

    ##### obtenir la liste des cours de Course Discovery
    w = requests.get('http://ec2-52-60-175-178.ca-central-1.compute.amazonaws.com:18381/api/v1/courses?limit=400', auth=(settings.EDULIB_USER, settings.EDULIB_PWD)) ;

    ##### traiter le tout comme une structure JSON
    json_data  = w.json()

    ##### pretty print de la structure JSON
    json_pretty_poly  = json.dumps(json_data,  sort_keys=True, indent=4)

    ##### obtenir l'entree "results" de la structure JSON
    toto  = json_data
    toto2 = toto.get('results')

    ##### obtenir la date courante en format ISO
    current = datetime.now().isoformat()

    ##### obtenir la liste des course_runs dans l'entree "results"
    mylist = []
    for course in toto2:
       if course['course_runs']:
          y = course['course_runs']
          mylist.append(course)

    ##### filtrer les course_runs pour lequel le owner est l'institution demandee
    mylist2 = []
    for course in mylist:
       if course['owners']:
          y = course['owners']
          z = course['course_runs']
          #####print (z[0]['end'])
          #####print (y)
          #####print (y[0]['key'])
          #####print (school)
          if school in y[0]['key']:
             if z[0]['end']:
                yourdate_end = dateutil.parser.parse(z[0]['end'])
                z[0]['end_affiche'] = yourdate_end.strftime("%d %B %Y")
             if z[0]['start']:
                yourdate_start = dateutil.parser.parse(z[0]['start'])
                z[0]['start_affiche'] = yourdate_start.strftime("%d %B %Y")
             mylist2.append(course)


    ##### calcul du nombre de cours pour l'institution demandee
    #####long = len(mylist2)
    #####print "Nombre de cours HEC : %d" % long
    #####print ('')
    ##### number of courses is ok #####

    ##### extracting course runs  #####
    mylist3 = []
    for course in mylist2:
       if course['course_runs']:
          y = course['course_runs']
          mylist3.append(y)

    ##### calcul du nombre de cours
    long3 = len(mylist3)
    #print "Nombre de cours HEC : %d" % long3
    #print ('')
    ##### number of courses is ok #####

    ##### extracting first element of all courses #####
    mylist4 = []
    i = 0
    while i < long3:
       y = mylist3[i][0]
       #print y
       #print('')
       mylist4.append(y)
       i = i + 1

    ##### besoin contexte contenant 3 arrays: upcoming, current, done #####
    upcoming = []
    current  = []
    done     = []
    liste_totale = []

    ##### popule les 3 arrays selon les bons criteres #####
    for cours in mylist4:
        if cours['availability'] == "Upcoming" and not cours['hidden']:
           upcoming.append(cours)
        elif cours['availability'] == "Current" and not cours['hidden']:
             current.append(cours)
        elif cours['availability'] == "Archived":
             done.append(cours)

    ##### tri les 3 arrays selons les criteres EDUlib #####
    upcoming_by_start = sorted(upcoming, key=itemgetter('start'), reverse=True)
    current_by_start  = sorted(current, key=itemgetter('start'), reverse=True)
    done_by_start     = sorted(done, key=itemgetter('end'), reverse=True)

    ##### calcule la taille de chaque array #####
    #upcoming_len = len(upcoming)
    #current_len  = len(current)
    #done_len     = len(done)
    #print upcoming_len, current_len, done_len

    ##### ajouter les 3 arrays dans le contexte global #####
    liste_totale.append(upcoming_by_start)
    liste_totale.append(current_by_start)
    liste_totale.append(done_by_start)

    ##### ajouter le nom de l'institution courante
    ecole = ""
    if school is 'PolyMtl':
       ecole = "Polytechnique"
    elif school is 'UMontreal':
       ecole = "Université de Montréal"
    elif school is 'HEC':
       ecole = "Hautes Etudes Commerciales"
    liste_totale.append(ecole)

    ##### calcule la taille du contexte global  #####
    #totale_len = len(liste_totale)
    #print totale_len
    #print liste_totale

    ##### initialise le contexte global #####
    context = {'cours_non_finis': liste_totale}

    ##### je ramene le nom selon les templates #####
    if school is 'PolyMtl':
       school = "polymtl"
    elif school is 'UMontreal':
       school = "umontreal"
    elif school is 'HEC':
       school = "hec"

    template = 'catalog/' + school + '.html'
    #####print template

    ##### affichage du contexte via le template de l'institution #####
    return render(request, template, context)
    #return HttpResponse(json_pretty_poly, content_type="application/json")
    #return HttpResponse("DO I GET HERE")





def index(request):
    ###########z = requests.get('http://ec2-35-182-73-26.ca-central-1.compute.amazonaws.com:18381/api/v1/courses?limit=400', auth=('bigboss', 'Bar07Har')) ;
    ###########z = requests.get('http://ec2-52-60-175-178.ca-central-1.compute.amazonaws.com:18381/api/v1/courses?limit=400', auth=('bigboss', 'Bar07Har')) ;
    z = requests.get('http://ec2-52-60-175-178.ca-central-1.compute.amazonaws.com:18381/api/v1/courses?limit=400', auth=('bigboss', 'Bar07Har')) ;
    #w = requests.get('http://ec2-52-60-175-178.ca-central-1.compute.amazonaws.com:18381/api/v1/course_runs/?q=ORG:Polymtl', auth=('bigboss', 'Bar07Har')) ;
    json_data  = z.json()
    #json_data2 = w.json()
    json_pretty  = json.dumps(json_data,  sort_keys=True, indent=4)
    #json_pretty2 = json.dumps(json_data2, sort_keys=True, indent=4)
    #
    # adding filtering
    #
    toto  = json_data
    #####print "Nombre de cours chez EDUlib : %d" % toto.get('count')
    #####print ('')
    current = datetime.now().isoformat()
    #####print ("Date actuelle")
    #####print (current)
    ####print ('')

    toto2 = toto.get('results')


    #for course in toto2:
    #   if course['owners']:
    #      y = course['owners']
    #      #print(y)
    #      #if "UMontreal" in y[0]['key']:
    #      #if "HEC" in y[0]['key']:
    #      if "Sherbroo" in y[0]['key']:
    #         print(course['title'])

    mylist = []
    for course in toto2:
       if course['course_runs']:
          y = course['course_runs']
          if y[0]['start']:
             if y[0]['end']:
                if ((y[0]['start'] < current and y[0]['end'] > current) or (y[0]['start'] > current)) and (y[0]['availability'] == "Current" or y[0]['availability'] == "Upcoming"):
                    mylist.append(y)
             else:
                if (y[0]['start'] > current) and (y[0]['availability'] == "Current" or y[0]['availability'] == "Upcoming"):
                   mylist.append(y)
          

    mylist2 = mylist

    mylist3 = []
    long = len(mylist2)
    #####print ("Nombre de cours non termines : %d" % long)
    #####print ('')
    i = 0
    while i < long:
       y = mylist2[i]
       #print(y[0]['end'])
       #print(y[0])
       #print('')

       if y[0]['end']:
          yourdate_end = dateutil.parser.parse(y[0]['end'])
          y[0]['end_affiche'] = yourdate_end.strftime("%d %B %Y")
       if y[0]['start']:
          yourdate_start = dateutil.parser.parse(y[0]['start'])
          y[0]['start_affiche'] = yourdate_start.strftime("%d %B %Y")

       mylist3.append(y[0])
       i = i + 1 

    # du debut le plus tard au plus tot
    mylist3_by_end = sorted(mylist3, key=itemgetter('start'), reverse=True)
    #mylist3_by_end = sorted(mylist3, key=itemgetter('end'), reverse=False)

    long = len(mylist3_by_end)
    #####print ("Liste des cours non termines : ")
    i = 0
    while i < long:
       y = mylist3_by_end[i]
       #####print(y['key'])
       #####print(y['end'])
       i = i + 1 
       #####print ('')

    context = {'cours_non_finis': mylist3_by_end}

    return render(request, 'catalog/index.html', context)
    #return HttpResponse(json_pretty, content_type="application/json")
