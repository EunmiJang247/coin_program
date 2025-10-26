from django.apps import AppConfig
import os

class TradeappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tradeapp'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
             # 실제 메인 프로세스에서만 실행됨
            try:
                import tradeapp.scheduler as scheduler
                scheduler.start()
            except Exception as e:
                print(f"Scheduler start error: {e}")