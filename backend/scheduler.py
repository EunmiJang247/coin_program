from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from apscheduler.triggers.cron import CronTrigger
import logging
import time
from django.db import close_old_connections
import traceback
from tradeapp.views_scheduler import check_current_price

logger = logging.getLogger('scheduler')

def start():
	scheduler = BackgroundScheduler()
	scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
	# Django의 데이터베이스에서 job을 읽어오지 않고, 기본적으로 메모리에서만 작업을 관리하게 됩니다
	register_events(scheduler)

	# 카메라 작동확인 및 사진 업데이트
	@scheduler.scheduled_job('interval', seconds=3, name='notification_report_create', id='notification_report_create')
	def notification_report_create():
		try:
			start_time = time.time()
			check_current_price()

		except Exception as e:
			pass
			logger.error(e)
			logger.error(traceback.format_exc())
			
	scheduler.start()