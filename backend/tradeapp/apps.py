from django.apps import AppConfig

class TradeappConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'tradeapp'
	
	def ready(self):
		try:
			import tradeapp.scheduler as scheduler
			scheduler.start()
		except Exception as e:
			print(f"Scheduler start error: {e}")