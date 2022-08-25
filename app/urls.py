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
    path('login/',views.login, name="login"),
    path('postsign/',views.index, name="validate"),
    path("register/",views.signup ,name="register"),
    path("signup/",views.signup,name="registered"),
    path("ph/",views.ph,name="ph"),
    path("temperature/",views.temperature,name="temperature"),
    path("turbidity/",views.turbidity,name="turbidity"),
    path("super_admin/",views.super_admin,name="super_admin"),
    path("norm_admin/",views.norm_admin,name="norm_admin"),
    path("download/",views.export,name="download"),
    path("testing/",views.testing,name="testing"),
    path("register_test/",views.register_test,name="register_test")
]
