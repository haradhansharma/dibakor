from django.apps import AppConfig
from django.conf import settings



class FeedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feed'
    
    
    def ready(self):
        # from jobs.updater import ScheduleParse, SendNewsLatter    
        from jobs.jobs import schedule_api   
        
        schedule_api()
        
