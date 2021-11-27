from datetime import datetime, time
from django.utils import timezone
import sys
from .jobs import schedule_api, schedule_api_newsletter
import logging
from django.conf import settings
from feed.models import *
from django_cron import CronJobBase, Schedule

class ScheduleParse(CronJobBase):
    RUN_EVERY_MINS = 2
    RUN_AT_TIMES = [ExSite.on_site.all()[0].feed_fetch_time]
    RETRY_AFTER_FAILURE_MINS = 5
    MIN_NUM_FAILURES = 3    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'jobs.schedule_parse' 
    def do(self):    
        schedule_api()
    
class SendNewsLatter(CronJobBase):
    RUN_EVERY_MINS = 3    
    RUN_AT_TIMES = [ExSite.on_site.all()[0].newsletter_send_time]
    RETRY_AFTER_FAILURE_MINS = 5
    MIN_NUM_FAILURES = 3    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'jobs.send_news_letter' 
    def do(self):    
        schedule_api_newsletter()
# This is the cron comamnd for cpanel    
# * * * * * source /home/sincehence/.bashrc && source /home/sincehence/virtualenv/dibakor.com/3.7/bin/activate && python /home/sincehence/dibakor.com/manage.py runcrons > /home/dibakor.com/cronjob.log    


# logger = logging.getLogger(__name__)
# def start():
#     DjangoJobExecution.objects.delete_old_job_executions(max_age=604_800)
#     scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG, timezone=settings.TIME_ZONE)
#     scheduler.add_job(schedule_api, 'interval', minutes=200, id="schedule_api", jobstore='default', max_instances=1, replace_existing=True)
#     logger.info("Added job 'schedule_api'.")
#     scheduler.add_job(schedule_api_newsletter, 'interval', minutes=200, id="schedule_api_newsletter", jobstore='default', max_instances=1,replace_existing=True)
#     logger.info("Added job: 'schedule_api_newsletter'." )
#     try:
#         logger.info("Starting scheduler...")
#         scheduler.start()
#     except KeyboardInterrupt:
#         logger.info("Stopping scheduler...")
#         scheduler.shutdown()
#         logger.info("Scheduler shut down successfully!")
# def start():
    #     if settings.DEBUG:
    #         # Hook into the apscheduler logger
    #         logging.basicConfig()
    #         logging.getLogger('apscheduler').setLevel(logging.DEBUG)
            
    #     scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG, timezone="Asia/Dhaka")
    #     # scheduler.add_jobstore(DjangoJobStore(), "default")
    #     scheduler.add_job(schedule_api, "cron", hour=ExSite.on_site.all()[0].feed_fetch_time, id="schedule_api", name='fetch_data', jobstore='default', replace_existing=True)
    #     scheduler.add_job(schedule_api_newsletter, "cron", hour=ExSite.on_site.all()[0].newsletter_send_time, id="schedule_api_newsletter",  name='send_news_letter', jobstore='default', replace_existing=True)  
    #     register_events(scheduler)  
    #     scheduler.start()
        


  