from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from apscheduler.triggers.cron import CronTrigger
import logging
import time
import traceback
from tradeapp.views_scheduler import check_current_price

logger = logging.getLogger('scheduler')

def start():
	scheduler = BackgroundScheduler(timezone='Asia/Seoul')
	scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
	register_events(scheduler)

	# 카메라 작동확인 및 사진 업데이트
	@scheduler.scheduled_job('interval', minutes=120, name='notification_report_create', id='notification_report_create')
	def notification_report_create():
		try:
			start_time = time.time()
			logger.info('check_weather_state =========================start')
			check_current_price()
			logger.info(f'check_weather_state ========================end {time.time()-start_time} second elapsed')

		except Exception as e:
			pass
			logger.error(e)
			logger.error(traceback.format_exc())
			
	scheduler.start()