from django.contrib import messages
from django.core import mail
from django.core.mail import BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from feed.models import Subscriber
from .forms import SubscriberForm
import random
from feed.models import *
from django.db.models import Count


def common(request):    
    return {   
        'dep_list':Department.objects.all(),
        'pc_list': ParserCategory.objects.all(),
        'slides':SlideShow.objects.all(),
        'info_list': Informaion.objects.all(),
        'parser_list': Parser.objects.all(),
        'search_terms': SearchRecord.objects.all().values('term').annotate(total=Count('term')).order_by('-total')[:50],
        'rst':Blocks.objects.filter(position__exact = 'rst')[0],
        'lst':Blocks.objects.filter(position__exact = 'lsh')[0],
        'site':ExSite.on_site.all()[0]      
        
    }
    

def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

@csrf_exempt
def subsform(request):      
    a = str(request).split('/')      
    if 'admin' not in  a:   
        if request.method == 'POST':
            s_form = SubscriberForm(request.POST)        
            if s_form.is_valid():
                # mail parameter   
                # param =  ExtendSite.objects.all()[0]
                site_mail= ExSite.on_site.all()[0].email
                host = ExSite.on_site.all()[0].email_host
                port=ExSite.on_site.all()[0].email_port
                userkey=ExSite.on_site.all()[0].email_host_user
                passkey=ExSite.on_site.all()[0].email_host_pass  
                
                to_email = s_form.cleaned_data['s_email'] 
                to_department = s_form.cleaned_data['s_department'] 
                subject = 'Newsletter Confirmation'               
                try:
                    subscribers = Subscriber.objects.filter(s_email__exact = to_email)[0]
                except:
                    subscribers = False
               
                if not subscribers:
                    confirm_num = random_digits()
                    sub = Subscriber(s_email=to_email, s_department=to_department, conf_num = confirm_num)            
                    sub.save()
                    messages.success(request, f'{to_email} added successfully!') 
                    message = f'Dear {to_email}, \n\n'              
                    message += 'Thank you for signing up for my email newsletter! Please complete the process by <a href="{}?s_email={}&conf_num={}"> clicking here to confirm your registration</a>.\n'.format(request.build_absolute_uri('/confirm/'), to_email, confirm_num )
                    message += f'Best Regards \n\n {ExSite.on_site.all()[0].site_meta}'
                    with mail.get_connection(host=host, port=port,username=userkey,password=passkey) as connection:
                        try:
                            mail.EmailMessage( subject, message, site_mail, [to_email], connection=connection,).send()                    
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                else: 
                    if subscribers.s_email == to_email:
                        if subscribers.confirmed:
                            messages.success(request, f'{to_email} already confirmed!')                                                          
                        else:                        
                            messages.success(request, f'{to_email} listed already, Please Check you mail and confirm!')
                            confirm_num = subscribers.conf_num
                            sub = Subscriber.objects.filter(s_email=to_email)            
                            sub.update(s_department=to_department)
                            message = f'Dear {to_email}, \n\n'      
                            message += 'Welcome again! Please complete the process by <a href="{}?s_email={}&conf_num={}"> clicking here to confirm your registration</a>.\n'.format(request.build_absolute_uri('/confirm/'), to_email, confirm_num )
                            message += f'Best Regards \n\n {ExSite.on_site.all()[0].site_meta}'
                            with mail.get_connection(host=host, port=port,username=userkey,password=passkey) as connection:
                                try:
                                    mail.EmailMessage( subject, message, site_mail, [to_email], connection=connection,).send()                    
                                except BadHeaderError:
                                    return HttpResponse('Invalid header found.')
            else:
                messages.error(request, 'Invalid form submission.')
                messages.error(request, s_form.errors)
        else:
            s_form = SubscriberForm()
        context = {
                    's_form':s_form,                                     
                }
        return context
    else:
        s_form = SubscriberForm()
        context = {
                    's_form':s_form,                                     
                }
        return context
             
  
   