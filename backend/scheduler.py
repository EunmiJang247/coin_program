from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.jobstores import register_events

from tradeapp.views_scheduler import check_current_price
from django_apscheduler.models import DjangoJob

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

def start_scheduler(sender, **kwargs):
    if not scheduler.running:
        DjangoJob.objects.all().delete()
        register_events(scheduler)
        scheduler.start()

def hi():
    check_current_price()

# 기존 작업을 확인하고 삭제한 후 추가
job_id = 'hidd'
existing_job = scheduler.get_job(job_id)
if existing_job:
    scheduler.remove_job(job_id)

scheduler.add_job(hi, 'interval', seconds=5, id=job_id)

