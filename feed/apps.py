from django.apps import AppConfig
from django.conf import settings


class FeedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feed'
    
    def ready(self):
        from jobs import updater
        if settings.SCHEDULER_AUTOSTART:
            updater.start()
        # updater.send_auto_news_letter()
