# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.landing, name='home'),
    path('chartsxddd/',views.singleLineChart,name='chart'),
    
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
    path('login/',views.trail, name="validate"),
    path('postsign/',views.index, name="validate"),
    path("register/",views.signup ,name="register"),
    path("signup/",views.signup,name="registered"),
    path("ph/",views.ph,name="ph"),
    path("temperature/",views.temperature,name="temperature"),
    path("turbidity/",views.turbidity,name="turbidity")


    #ph
    # path('ph/',views.ph, name='ph')

]
