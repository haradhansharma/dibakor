from feedparser import exceptions
import requests
from bs4 import BeautifulSoup
import lxml
import html5lib
from feed.models import *
import feedparser
import datetime
from django.contrib.sites.models import Site


def schedule_api():  
    parser_data = Parser.objects.filter(activate = True)
    for pd in parser_data:
        parser_url = pd.feed_url
        parser_feed = Parser.objects.get(id = pd.id)
        parser_feed_type = pd.parser_type      
        
        if parser_feed_type == 'rss':
            feed_response = requests.get(parser_url)
            if feed_response.status_code == 200:
                soup = BeautifulSoup(feed_response.content, 'xml')            
                items = []
                if soup.find_all('item'):
                    items = soup.find_all('item')[:25]
                elif soup.find_all('entry'):
                    items = soup.find_all('entry')[:25]
                else:
                    pass
                
                existing = ParsedData.objects.filter(feeder_id__exact = pd.id)
                rs = all(elem in items for elem in existing)               
                if rs:          
                    for item in items:               
                        title = item.find('title').text if item.find('title').text else ''
                        link = item.find('link').text if item.find('link').text else ''                    
                        pubdate = item.find('pubDate').text if item.find('pubDate').text else item.find('published').text if item.find('published').text else datetime.datetime.now()
                        description = item.find('description').text if item.find('description').text else ''                        
                        
                        fetched = ParsedData(feeder=parser_feed, title=title.strip(), link=link.strip(), pubdate=pubdate.strip(), description= description.strip()[:100])                  
                        fetched.save()
            else:            
                soup = feedparser.parse(parser_url)
                items = []
                if soup.entries:
                    items = soup.entries[:25] 
                else:
                    pass   
                
                existing = ParsedData.objects.filter(feeder_id__exact = pd.id) 
                rs = all(elem in items for elem in existing)               
                if rs:               
                    for item in items:                    
                        title = item.title if item.title else ''                    
                        link = item.link if item.link else ''                    
                        pubdate = item.published if item.published else datetime.datetime.now()
                        description = item.summary if item.summary else ''  
                        
                        fetched = ParsedData(feeder=parser_feed, title=title.strip(), link=link.strip(), pubdate=pubdate.strip(), description= description.strip()[:100])                      
                        fetched.save()                 
                    
        
        if parser_feed_type == 'youtube':
            soup = feedparser.parse(parser_url)            
            items = []
            if soup.entries:
                items = soup.entries[:25] 
            else:
                pass
            
            existing = ParsedData.objects.filter(feeder_id__exact = pd.id)
            rs = all(elem in items for elem in existing)               
            if rs:  
                for item in items:                
                    title = item.title if item.title else ''                
                    link = item.link if item.link else ''                
                    pubdate = item.published if item.published else datetime.datetime.now()
                    description = item.summary if item.summary else ''  
                    
                    fetched = ParsedData(feeder=parser_feed, title=title.strip(), link=link.strip(), pubdate=pubdate.strip(), description= description.strip()[:100])    
                    fetched.save() 
            
        
        if parser_feed_type == 'url':
            pass  
        
def schedule_api_newsletter():
    
    # mail parameter
    site_meta= ExSite.on_site.all()[0].site_meta
    site_mail= ExSite.on_site.all()[0].email
    host = ExSite.on_site.all()[0].email_host
    port=ExSite.on_site.all()[0].email_port
    userkey=ExSite.on_site.all()[0].email_host_user
    passkey=ExSite.on_site.all()[0].email_host_pass      
    
    subject = "Today's feeds" 
    domain = Site.objects.get_current().domain   
    
    
    deps = Department.objects.all()
    for dep in deps:    
        subs = Subscriber.objects.filter(s_department = dep.id)
        prcs = ParserCategory.objects.filter(department__in = [sub.s_department for sub in subs])
        prs = Parser.objects.filter(category__in = [prc.id for prc in prcs])
        pds = ParsedData.objects.filter(feeder__in = [pr.id for pr in prs])
        
        
        for s in subs.iterator():
            to_email = s.s_email
            conf_num = s.conf_num
            message = '<div style="display: block; max-width:580px;padding:10px; margin: 0 auto!important; border: 1px solid #0396A6; background:#A0EAF2;">'
            message += f"<p>Dear {to_email},</p>"
            message += f'<a href="{domain}" style="display:block;padding:10px;background:#0396A6;color:#E8CF91;text-align:center; margin:10px auto!important; overflow:hidden; width:120px; text-decoration:none;" >Visit {site_meta}</a>'
            message += f'<div style="display: block; max-width:500px;padding:10px; margin: 0 auto!important; border: 1px solid #F2B705; background:#E8CF91;">'
            message += f'<p>Below are the feeds collected for you!...</p><ul>'
            for f in pds.iterator():
                message += f'<li><a style="font-weight: bold;text-decoration: none; color:#0396A6;" href="{f.link}"> {f.title}-{f.created} </a> <p style="color: lightslategray;"> {f.description}</p></li>' 
            message += f'</ul></div><p>Best Regards </p><br><p>{ExSite.on_site.all()[0].site_meta}</p><p>{domain}</p>'    
            message += f'<div style="color:white; font-size:10px; text-align:center; display:block;width:400px;padding:5px;margin:0 auto!important;">Don\'t like these emails?<a href="{domain}/delete/?email={to_email}&conf_num={conf_num}">Unsubscribe</a></div></div>'            
                   
            
            with mail.get_connection(host=host, port=port,username=userkey,password=passkey) as connection:
                try:
                    msg = mail.EmailMessage(subject, message, site_mail, [to_email], connection=connection,)   
                    msg.content_subtype = "html"
                    msg.send()               
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')      
                
            

    