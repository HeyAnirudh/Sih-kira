# -*- encoding: utf-8 -*-

"""
Copyright (c) 2019 - present AppSeed.us
"""

from asyncio.windows_events import NULL
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#firestore intitializations
credJson = credentials.Certificate("./app/ServiceAccountKey.json")
firebase_admin.initialize_app(credJson)
db = firestore.client()
db.collection('test').document('testdoc').set({"name":"keshav","age":699})



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



def index(request):
    email=request.POST.get("email")
    passw = request.POST.get("pass")
    print(email)
    try:
        user = auth.sign_in_with_email_and_password(email,passw)
    except:
        message = "invalid cerediantials"
        return render(request,"nahi.html",{"msg":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    # return render(request,"Home.html",{"email":email})
   

    
    context = {}
    context["temp"]=database.child('Data').child('Temerature').get().val()
    context["ph"]=database.child('Data').child('ph').get().val()
    context["turbi"]=database.child('Data').child('Turbidity').get().val()
    context["email"]=email
    res=db.collection('Userdb').document(email).get()
    if res.exists:

        print(res.to_dict())
        data=res.to_dict()

    else:
        print("not")
    context["school_name"]=data["school_name"]


    
    

    ph_cal=pH_Calc(context["ph"])
    turb_cal= turb_Calc(context["turbi"])
    temp_cal=temp_Calc(context["temp"])
    if ph_cal < 5 or turb_cal < 6 or temp_cal < 5 :
        context["ans"]=0
    else:
        context["ans"] = ((pH_Calc(context["ph"]) + turb_Calc(context["turbi"]) + temp_Calc(context["temp"]))//3)*10


    


    
    db.collection('testSensor').document().set(context)
    
    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    print(request.user.username)
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
@login_required(login_url="/login/")
def singleLineChart(request):

    
    data = db.collection('testSensor').get()
    
    temperatureData = []
    phData=[]
    turbidityData=[]
    for doc in data:
        a= doc.to_dict()
        temp=a['temp']
        ph=a['ph']
        turb=a['turbi']
        temperatureData.append(temp)
        phData.append(ph)
        turbidityData.append(turb)
    
    chartContext = {
        "temperatureData":temperatureData,
        "phData":phData,
        "turbidityData":turbidityData
    }
    html_template = loader.get_template( 'charts.html' )
    return render(request ,'charts.html',chartContext)


def trail(request):
    return render(request,'login.html')


def signup(request):
    sch_name=request.POST.get("School_Name")
    sch_id= request.POST.get("School_id")
    email=request.POST.get("email")
    passw = request.POST.get("password")
    if sch_name != None or sch_id != None or email != None or passw!=None:
        db.collection('Userdb').document(email).set({"school_name":sch_name,"school_id":sch_id,"email":email,"Password":passw})
        print(sch_name)
        print(sch_id)
        print(email)
        print(passw)

        user=auth.create_user_with_email_and_password(email,passw)
        uid = user['localId']
        idtoken = request.session['uid']
        print(uid)
    
    return render(request,"regis.html")
    
def landing(request):
    return render(request,"landing.html")

def ph(request):
    return render(request,"ph.html")
    

