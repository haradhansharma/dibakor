from datetime import datetime, time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys
from .jobs import schedule_api, schedule_api_newsletter
import logging
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django.conf import settings



def start():
    if settings.DEBUG:
        # Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)
        
    scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)
    # scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(schedule_api, 'interval', hours=24, id="schedule_api", name='fetch_data', jobstore='default', replace_existing=True)
    scheduler.add_job(schedule_api_newsletter, 'interval', seconds=320000, id="schedule_api_newsletter",  name='send_news_letter', jobstore='default', replace_existing=True)  
    register_events(scheduler)  
    scheduler.start()
    


  