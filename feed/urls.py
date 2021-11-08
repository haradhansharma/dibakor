
from django.urls import path
from . import views
from django.shortcuts import render 
from django.views.generic import TemplateView



app_name = 'feed'
urlpatterns = [
    path('', views.feed, name='feed'),   
    path('confirm/', views.confirm, name='confirm'),
    path('delete/', views.delete, name='delete'),    
    path('dept/<slug:slug>', views.department_details, name='department-detail'),
    path('search/', views.Search.as_view(), name='search'),
    path('category/<slug:slug>', views.pc_detail, name='pc-detail'),
    path('parser/<slug:slug>', views.parserdetailview, name='parser-detail'),
    path('info/<slug:slug>', views.InformaionDetailView.as_view(), name='information'),
       
]

urlpatterns += [
    path('', lambda request: render(request, 'feed/content.html'))
] 