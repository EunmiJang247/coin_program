from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from apscheduler.triggers.cron import CronTrigger
import logging
import time
import traceback
from tradeapp.views_scheduler import check_current_price, scenario1_buy

logger = logging.getLogger('scheduler')

def start():
	scheduler = BackgroundScheduler(timezone='Asia/Seoul')
	scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
	register_events(scheduler)

	# 스케줄러 테스트
	@scheduler.scheduled_job('interval', minutes=10, name='notification_report_create', id='notification_report_create')
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

	# 시나리오1
	@scheduler.scheduled_job('interval', minutes=3, name='scenario1_schedule', id='scenario1_schedule')
	def scenario1_schedule():
		try:
			start_time = time.time()
			logger.info('scenario1 =========================start')
			scenario1_buy()
			logger.info(f'scenario1 ========================end {time.time()-start_time} second elapsed')

		except Exception as e:
			pass
			logger.error(e)
			logger.error(traceback.format_exc())
			
	scheduler.start()