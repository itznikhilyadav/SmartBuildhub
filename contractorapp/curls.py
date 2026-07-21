from django.urls import path
from . import views

urlpatterns=[
    path('contractordash/',views.contractordash,name='contractordash'),
    path('contractorlogout/',views.contractorlogout,name='contractorlogout'),
    path('contractorchangepass/',views.contractorchangepass,name='contractorchangepass'),
    path('contractorprofile/',views.contractorprofile,name='contractorprofile'),
    path('contractoredit/',views.contractoredit,name='contractoredit'), 
    path('contractorviewprojects/',views.contractorviewprojects,name='contractorviewprojects'), 
    path('applyproject/<id>',views.applyproject,name='applyproject'), 
    path('contractorapplications/',views.contractorapplications,name='contractorapplications'), 
]
