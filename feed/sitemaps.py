from django.contrib import sitemaps
from django.urls import reverse
from feed.models import *

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'daily' 

    def items(self):
        return ['feed:feed',  'feed:search',]

    def location(self, item):
        return reverse(item)
    
class DeptSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        return Department.objects.all()    
    
    def lastmod(self, obj):
        return obj.created
        
    def location(self,obj):
        return '/dept/%s' % (obj.slug)
    
class ParserCategorySitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        return ParserCategory.objects.all()  
    
    def lastmod(self, obj):
        return obj.created  
        
    def location(self,obj):
        return '/category/%s' % (obj.slug) 
       
class ParserSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        return Parser.objects.all()  
    
    def lastmod(self, obj):
        return obj.created  
        
    def location(self,obj):
        return '/parser/%s' % (obj.slug) 
    
class InformaionSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        return Informaion.objects.all()  
    
    def lastmod(self, obj):
        return obj.created  
        
    def location(self,obj):
        return '/info/%s' % (obj.slug)         
    
class PdSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        return ParsedData.objects.all()   
    
    def lastmod(self, obj):
        return obj.created
        
    def location(self,obj):
        return '/pd/%s' % (obj.id)        