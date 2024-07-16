from django.apps import AppConfig
from django.conf import settings

class TradeappConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'tradeapp'
	def ready(self):
		from django.db.models.signals import post_migrate
		from scheduler import start_scheduler, scheduler
		post_migrate.connect(start_scheduler, sender=self)
		scheduler.start()