# from django.conf.urls import url
from django.urls import re_path as url
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
   url(r'^$', views.login,name='login'),
   url(r'^patientlist/', views.patientlist, name='patientlist'),
   url(r'^logout', views.logout, name="logout"),
   url(r'^Login', views.Login, name='Login'),
   # url(r'^homepage/', views.homepage, name='homepage'),
   url(r'^reset', views.reset, name='reset'),
   # url(r'^sub/',views.sub,name="sub/"),
   url(r'^presc',views.presc,name='presc'),
   url(r'^O2update', views.O2update, name='O2update'),
   url(r'^medupdate', views.medupdate, name='medupdate'),
   url(r'^sub',views.sub,name="sub"),
   url(r'^movepatient', views.movepatient, name='movepatient'),
   url(r'^secondarypatient', views.secondarypatient, name='secondarypatient'),
   url(r'^deletesecondary', views.deletesecondary, name='deletesecondary'),
   url(r'^dischargepatient', views.dischargepatient, name='dischargepatient'),


   path("<str:ID>", views.patientdetails, name='patientdetails'),
]