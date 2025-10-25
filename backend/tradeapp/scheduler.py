from apscheduler.schedulers.background import BackgroundScheduler  # schedulers → apscheduler
from tradeapp.services import service_get_all_favorite_coins_rsi, service_send_telegram_message  # backend.tradeapp → tradeapp
from django_apscheduler.jobstores import register_events, DjangoJobStore
from apscheduler.triggers.cron import CronTrigger
import logging
import datetime

logger = logging.getLogger('scheduler')

def start():
	scheduler = BackgroundScheduler(timezone='Asia/Seoul')
	scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
	register_events(scheduler)

	# 스케줄러 테스트
	@scheduler.scheduled_job('interval', seconds=10, name='test', id='test')
	def test():
		try:
			print('scheduler test', datetime.datetime.now())
		except Exception as e:
			pass
			logger.error(e)
   
	@scheduler.scheduled_job('interval', seconds=10, name='rsi_check', id='rsi_check')
	def check_favorite_rsi():
		try:
			results = service_get_all_favorite_coins_rsi('15m')
			
			# 과매수/과매도 상황 찾기
			overbought = [r for r in results if r.get('rsi') and r['rsi'] > 90]
			oversold = [r for r in results if r.get('rsi') and r['rsi'] < 29]
			
			if overbought:
				overbought_list = []
				for coin in overbought:
					overbought_list.append(f"{coin['symbol']}: {coin['rsi']}")
				
				message = f"🔴 과매수 신호 감지!\n" + "\n".join(overbought_list)
				print(f"🔴 과매수: {overbought_list}")
				
				try:
					service_send_telegram_message(message)
				except Exception as telegram_error:
					logger.error(f'텔레그램 전송 실패 (과매수): {telegram_error}')
			
			if oversold:
				oversold_list = []
				for coin in oversold:
					oversold_list.append(f"{coin['symbol']}: {coin['rsi']}")
				
				message = f"🟢 과매도 신호 감지!\n" + "\n".join(oversold_list)
				print(f"🟢 과매도: {oversold_list}")
				
				try:
					service_send_telegram_message(message)
				except Exception as telegram_error:
					logger.error(f'텔레그램 전송 실패 (과매도): {telegram_error}')
				
		except Exception as e:
			logger.error(f'RSI check error: {e}')

	scheduler.start()