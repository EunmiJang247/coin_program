from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.jobstores import register_events

from tradeapp.views_scheduler import check_current_price
from django_apscheduler.models import DjangoJob

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

def start():
    if not scheduler.running:
        DjangoJob.objects.all().delete()
        register_events(scheduler)
        scheduler.start()

def hi():
    check_current_price()

scheduler.add_job(hi, 'interval', seconds=5, id='hidd')
