from django.http import request
from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib import messages
from feed.forms import SearchForm
from . models import *
from django.views.generic.base import TemplateView
from django.views import generic, View
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def slideshow(request):
    
    return render(request, 'feed/slideshow.html', {'slides':SlideShow.objects.all()})
    
def confirm(request):
    sub = Subscriber.objects.get(s_email=request.GET['s_email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        return render(request, 'feed/confirm.html', {'s_email': sub.s_email, 'action': 'confirmed'})
    else:
        return render(request, 'feed/confirm.html', {'s_email': sub.s_email, 'action': 'denied'})
    
def delete(request):
    sub = Subscriber.objects.get(s_email=request.GET['s_email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.delete()
        return render(request, 'feed/delete.html', {'s_email': sub.s_email, 'action': 'unsubscribed'})
    else:
        return render(request, 'feed/delete.html', {'s_email': sub.s_email, 'action': 'denied'}) 

def feed(request):
    parse_data = ParsedData.objects.all().order_by('-created')
    paginator = Paginator(parse_data, ExSite.on_site.all()[0].pagination_para)
    page_number = request.GET.get('page')
    
    
    
    try:
        parse_data = paginator.get_page(page_number)
    except PageNotAnInteger :
        parse_data = paginator.get_page(1)
    except EmptyPage:
        parse_data = paginator.get_page(paginator.num_pages) 
    context = {        
        'parsed': parse_data,        
    }
    return render(request, 'feed/feed.html', context=context)


    
def department_details(request, slug):
    dep_list = get_object_or_404(Department, slug = slug) 
    pc_list = ParserCategory.objects.filter(department = dep_list.id) 
    if pc_list:
        for pl in pc_list:         
            parser = Parser.objects.filter(category = pl.id).distinct()
            for p in parser:
                parse_data = ParsedData.objects.filter(feeder = p.id).order_by('-created')
                paginator = Paginator(parse_data, ExSite.on_site.all()[0].pagination_para)
                page_number = request.GET.get('page')
                
                try:
                    parse_data = paginator.get_page(page_number)
                except PageNotAnInteger :
                    parse_data = paginator.get_page(1)
                except EmptyPage:
                    parse_data = paginator.get_page(paginator.num_pages)                              
                
                context = {        
                    'parsed': parse_data,
                    'meta_title': dep_list.name                        
                }        
                return render(request, 'feed/dep_detail.html', context=context) 
    else:
        pass
    context = {                   
                     
            }       
    
    return render(request, 'feed/dep_detail.html', context=context) 

class Search(View):
    template_name = 'feed/search.html'
    def get(self, request, *args, **kwargs):
        search_form = SearchForm(self.request.GET)        
        if search_form.is_valid():
            query = search_form.cleaned_data['query']            
            ip = request.META['REMOTE_ADDR'] + '(' + request.META['HTTP_USER_AGENT'] + ')'
                        
            sr = SearchRecord(term = query, ip = ip)
            sr.save()
            
            parse_data = ParsedData.objects.order_by('-pk').filter(Q(title__icontains=query)|Q(description__icontains = query))
            paginator = Paginator(parse_data, ExSite.on_site.all()[0].pagination_para)
            page_number = request.GET.get('page')
            
            try:
                parse_data = paginator.get_page(page_number)
            except PageNotAnInteger :
                parse_data = paginator.get_page(1)
            except EmptyPage:
                parse_data = paginator.get_page(paginator.num_pages)        
            
            context = {
                'parsed': parse_data,
                'meta_title': query,                  
            }
        else:
            return redirect('feed:feed')
        return render(request, self.template_name, context)
    
def left_sidebar(request):
    context={
        
                
    }
    return render(request, 'left_sidebar.html', context)

class InformaionDetailView(generic.DetailView):
    model = Informaion
    template_name = 'feed/information_detail.html'
    
    

    
def parserdetailview(request, slug):
    
    parser =get_object_or_404(Parser, slug = slug)    
    parse_data = ParsedData.objects.filter(feeder = parser.id).order_by('-created')    
    paginator = Paginator(parse_data, ExSite.on_site.all()[0].pagination_para)
    page_number = request.GET.get('page')
    
    try:
        parse_data = paginator.get_page(page_number)
    except PageNotAnInteger :
        parse_data = paginator.get_page(1)
    except EmptyPage:
        parse_data = paginator.get_page(paginator.num_pages)        
    
    context = {
        'parsed': parse_data,  
        'meta_title':parser.feed_name                
    }
     
    return render(request, 'feed/parser_rs.html', context)        
    
def pc_detail(request, slug):
    pc_list = get_object_or_404(ParserCategory, slug = slug)
    parser = Parser.objects.filter(category = pc_list.id)
    
    if parser:    
        for p in parser:
            parse_data = ParsedData.objects.filter(feeder = p.id).order_by('-created')
            paginator = Paginator(parse_data, ExSite.on_site.all()[0].pagination_para)
            page_number = request.GET.get('page')
            
            try:
                parse_data = paginator.get_page(page_number)
            except PageNotAnInteger :
                parse_data = paginator.get_page(1)
            except EmptyPage:
                parse_data = paginator.get_page(paginator.num_pages)   
            context = {        
                'parsed': parse_data,
                'meta_title': pc_list.name  
                       
            }
        return render(request, 'feed/pc_detail.html', context)     
    else:
        context = {  
                   'meta_title': pc_list.name              
                      
            }
        
        return render(request, 'feed/pc_detail.html', context) 
    
  
        
                
    
         
    

            
     


        
            






