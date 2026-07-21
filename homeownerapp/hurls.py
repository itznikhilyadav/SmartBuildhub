from django.urls import path
from . import views

urlpatterns=[
     path('homeownerdash/',views.homeownerdash,name='homeownerdash'),
     path('homeownerlogout/',views.homeownerlogout,name='homeownerlogout'),
     path('homechange_pass/',views.homechange_pass,name='homechange_pass'),
     path('homeownerprofile/',views.homeownerprofile,name='homeownerprofile'),
     path('homeowneredit/',views.homeowneredit,name='homeowneredit'),
     path('addproject/',views.addproject,name='addproject'),
     path('homeownerviewprojects/',views.homeownerviewprojects,name='homeownerviewprojects'),
     path('homeownerviewapplications/<id>',views.homeownerviewapplications,name='homeownerviewapplications'),
     
     
     
     
]