# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import pyrebase
import firebase_admin
from firebase_admin import credentials



config= {
  "apiKey": "AIzaSyBOmFCtJkyO3cGgIGFC2OuDo5UL5NltRbs",
  "authDomain": "hydrosense-2cc3a.firebaseapp.com",
  "databaseURL": "https://hydrosense-2cc3a-default-rtdb.firebaseio.com",
  "projectId": "hydrosense-2cc3a",
  "storageBucket": "hydrosense-2cc3a.appspot.com",
  "messagingSenderId": "779850611309",
  "appId": "1:779850611309:web:b1d7aa93dfb68ab113dd64",
}
firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
database=firebase.database()
def pH_Calc(pH):
    return 10 if pH == 7 else int(10-(abs(pH - 7)/0.5)*2) 


def turb_Calc(turb):
    if turb > 0 and turb < 0.4:
        return 10
    elif turb > 0.4 and turb < 0.6:
        return 8
    elif turb > 0.6 and turb < 0.8:
        return 4
    elif turb > 0.8 and turb < 1.0:
        return 2
    else:
        return 0

def temp_Calc(temp):
    if temp in range(18,35):
        return 10
    elif temp in range(35,45) or temp in range(0,18):
        return 8
    elif temp in range(45,55):
        return 6
    elif temp in range(55,65):
        return 4
    else:
        return 2


def waterQuality():
    pH = 7
    turb = 0.22222
    temp = 22
    ans = (pH_Calc(pH) + turb_Calc(turb) + temp_Calc(temp))//3

    return ans

print(waterQuality())
@login_required(login_url="/login/")
def index(request):

    
    context = {}
    context['segment'] = 'index'
    context["temp"]=database.child('Data').child('Temerature').get().val()
    context["ph"]=database.child('Data').child('ph').get().val()
    context["turbi"]=database.child('Data').child('Turbidity').get().val()
    context["ans"] = (pH_Calc(context["ph"]) + turb_Calc( context["turbi"]) + temp_Calc(context["temp"]))//3

    

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
