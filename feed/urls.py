from django.contrib.sitemaps.views import sitemap
from django.urls import path
from . import views
from django.shortcuts import render 
from django.views.generic import TemplateView
from .sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

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
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
       
]

urlpatterns += [
    path('', lambda request: render(request, 'feed/content.html'))
] 