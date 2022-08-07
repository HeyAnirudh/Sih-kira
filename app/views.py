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

# cred = credentials.Certificate("C:\\Users\\Anirudh soni\\Desktop\\Firebase key\\hydrosense-2cc3a-firebase-adminsdk-bl3a8-0481c30fb9.json")

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

@login_required(login_url="/login/")
def index(request):

    
    context = {}
    context['segment'] = 'index'
    context["temp"]=database.child('Data').child('Temerature').get().val()
    context["ph"]=database.child('Data').child('ph').get().val()
    context["turbi"]=database.child('Data').child('Turbidity').get().val()

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
