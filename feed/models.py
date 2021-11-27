from django.db import models
from django.urls.base import reverse
from django.utils.translation import activate
from django.core import mail
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from colorfield.fields import ColorField
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

class SlideShow(models.Model):
    pic = models.ImageField(upload_to = 'slides')
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    
    def __str__(self):
        return self.title
    
class Blocks(models.Model):
    POSITIONS = (
        ('lsh','Left SideBar Top'),
        ('rst', 'Right Sidebar Top'),        
    )
    
    pic = models.ImageField(upload_to = 'blocks')
    title = models.CharField(max_length=255) 
    description = models.TextField(null=True, blank=True) 
    position = models.CharField(max_length=500, choices=POSITIONS, default='lsh', unique=False)  
    
    def __str__(self):
        return self.title


class Department(models.Model):
    name = models.CharField(max_length=100)  
    slug = models.SlugField(unique=True, null=False, blank=False) 
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("feed:department-detail",  args=[str(self.slug)])
    

class ParserCategory(models.Model):
    name = models.CharField(max_length=100) 
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True) 
    slug = models.SlugField(unique=True, null=False, blank=False) 
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("feed:pc-detail", args=[str(self.slug)])
    

#Feed setting UI
class Parser(models.Model):
    PARSER_TYPE = (
        ('rss','RSS'),
        ('youtube', 'Youtube'),
        ('url', 'URL'),
    )
    feed_name = models.CharField(max_length=256)  
    category = models.ForeignKey(ParserCategory, on_delete=models.SET_NULL, null=True)     
    parser_type = models.CharField(max_length=500, choices=PARSER_TYPE, default='rss', unique=False)    
    feed_url = models.URLField()
    activate = models.BooleanField(default=True)
    ic_color = ColorField(default='#FF0000')
    slug = models.SlugField(unique=True, null=False, blank=False) 
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return self.feed_name
    
    def get_absolute_url(self):
        return reverse("feed:parser-detail", args=[str(self.slug)])
    
    
    
class ParsedData(models.Model):
    feeder = models.ForeignKey(Parser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500, null=True)    
    link = models.URLField(max_length=500, null=True)
    pubdate = models.CharField(max_length=256, null=True)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('feed:feed', args=[str(self.pk)])
    
class Subscriber(models.Model):
    s_email = models.EmailField(unique=True)
    s_department = models.CharField(max_length=5)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.s_email + " (" + ("not " if not self.confirmed else "") + "confirmed)"
    
    
        
    
class SearchRecord(models.Model):
    term = models.CharField(max_length=256)
    ip= models.CharField(max_length=256)
    
    def __str__(self):
        return self.term
    
    def get_absolute_url(self):        
        return reverse("feed:search_rec", args=[str(self.id)])
    
    
from django.templatetags.static import static
class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField(upload_to='uploaded_newsletters/')

    def __str__(self):
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")
    
    def send(self, request):        
        contents = static(self.contents.url)
        subscribers = Subscriber.objects.filter(confirmed=True)  
          
        site_mail= ExSite.on_site.all()[0].email
        host = ExSite.on_site.all()[0].email_host
        port=ExSite.on_site.all()[0].email_port
        userkey=ExSite.on_site.all()[0].email_host_user
        passkey=ExSite.on_site.all()[0].email_host_pass    
        for sub in subscribers:            
            to_email=sub.s_email
            subject=self.subject
            message = f'<img src="{contents}" alt="{subject}" title="{subject}" width="500" style="height: auto;">'
            message += ('<br><a href="{}?email={}&conf_num={}">Unsubscribe</a>.').format(request.build_absolute_uri('/delete/'), sub.s_email, sub.conf_num)
            with mail.get_connection(host=host, port=port,username=userkey,password=passkey) as connection:
                try:
                    msg = mail.EmailMessage( subject, message, site_mail, [to_email], connection=connection,)   
                    msg.content_subtype = "html"
                    msg.send()                    
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')  
           
class Informaion(models.Model):
    name = models.CharField(max_length=256)
    content = models.TextField()
    slug = models.SlugField(unique=True, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("feed:information", args=[str(self.slug)])
    
# extending djano site package
class ExSite(models.Model):
    site = models.OneToOneField(Site, primary_key=True, verbose_name='site', on_delete=models.CASCADE)
    site_meta = models.CharField(max_length=256)
    site_description = models.TextField(max_length=500)
    site_meta_tag =models.CharField(max_length=255)
    site_favicon = models.ImageField(upload_to='site_image')
    site_logo = models.ImageField(upload_to='site_image')
    slogan = models.CharField(max_length=150, default='Multitasking Living Machine')
    og_image = models.ImageField(upload_to='site_image')
    
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    feed_fetch_time = models.CharField(max_length=2, help_text="Put 0,6,12,18 like that")
    newsletter_send_time = models.CharField(max_length=2, help_text="Put 0,6,12,18 like that")
    location=models.CharField(max_length=120)
    facebook_link = models.URLField()
    twitter_link = models.URLField()
    linkedin_link = models.URLField()
    
    
    # custom email setting under site package
    email_host = models.CharField(max_length=256)
    email_port = models.CharField(max_length=256)
    email_host_user = models.EmailField()
    email_host_pass = models.CharField(max_length=256) 
    
    pagination_para = models.CharField(max_length=2, default=10)
    
    # It is implemented for future roadmap
    objects = models.Manager()
    on_site = CurrentSiteManager('site')
    
    def __str__(self):
        return self.site.__str__()   
            
            