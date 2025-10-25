from django.apps import AppConfig
from django.conf import settings

class TradeappConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'tradeapp'
	def ready(self):
		import tradeapp.scheduler as scheduler
		scheduler.start()