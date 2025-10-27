from apscheduler.schedulers.background import BackgroundScheduler  # schedulers → apscheduler
from tradeapp.services import service_get_all_favorite_coins_rsi, service_get_available_balance_usdt, service_get_futures_wallet_balances, service_klines, service_open_long_position, service_open_short_position, service_send_telegram_message, service_check_if_ihave_this_coin, service_close_position, service_get_rsi
import logging
import datetime

logging.getLogger('apscheduler').setLevel(logging.WARNING)
logger = logging.getLogger('scheduler')

def start():
	scheduler = BackgroundScheduler(timezone='Asia/Seoul')

	@scheduler.scheduled_job('interval', minutes=10, name='rsi_check', id='rsi_check')
	def check_favorite_rsi():
		try:
			service_send_telegram_message('10분마다 실행되는 생존 알림!')
			# 내가 가지고 있는 코인들을 한번 돈다
			my_wallet_positions = service_get_futures_wallet_balances()
			
			# 보유 중인 포지션들 매도 조건 확인
			for position in my_wallet_positions:
				try:
					symbol = position['symbol']
					entry_price = float(position['entryPrice'])
					current_price = float(position['markPrice'])
					position_amt = float(position['positionAmt'])
					
					# RSI 값 가져오기
					rsi_data = service_get_rsi(symbol, '15m')
					rsi_value = rsi_data.get('rsi') if rsi_data else None
					
					if rsi_value is None:
						continue
					
					# 매도 조건 확인
					should_sell = False
					sell_reason = ""
					
					if position_amt > 0:  # 롱 포지션
						# 현재가가 진입가보다 높고 RSI가 70 이상
						if current_price > entry_price and rsi_value >= 70:
							should_sell = True
							profit_percent = ((current_price - entry_price) / entry_price) * 100
							sell_reason = f"롱 포지션 익절 조건 만족 (진입가: {entry_price:.4f}, 현재가: {current_price:.4f}, RSI: {rsi_value:.2f}, 수익률: {profit_percent:.2f}%)"
					
					elif position_amt < 0:  # 숏 포지션
						# 현재가가 진입가보다 낮고 RSI가 30 이하
						if current_price < entry_price and rsi_value <= 30:
							should_sell = True
							profit_percent = ((entry_price - current_price) / entry_price) * 100
							sell_reason = f"숏 포지션 익절 조건 만족 (진입가: {entry_price:.4f}, 현재가: {current_price:.4f}, RSI: {rsi_value:.2f}, 수익률: {profit_percent:.2f}%)"
					
					# 매도 실행
					if should_sell:
						close_result = service_close_position(symbol, position_amt)
						if close_result and close_result.get('status') == 'success':
							sell_msg = f"💰 포지션 종료 성공!\n{symbol}\n{sell_reason}"
							service_send_telegram_message(sell_msg)
							logger.info(f"Position closed: {symbol}")
						else:
							error_msg = f"❌ 포지션 종료 실패: {symbol}"
							if close_result and close_result.get('error'):
								error_msg += f"\n오류: {close_result['error']}"
							service_send_telegram_message(error_msg)
							logger.error(error_msg)
				
				except Exception as position_error:
					logger.error(f'포지션 매도 확인 실패 {position.get("symbol", "Unknown")}: {position_error}')


			# 내 지갑을 확인해서 20usd 이하로 있으면 더이상 실행하지 않기
			if service_get_available_balance_usdt() < 20:
				service_send_telegram_message('지갑 잔액이 20 USDT 이하입니다. RSI 체크를 중단합니다.')
				return
			results = service_get_all_favorite_coins_rsi('15m')
			
			# 과매수/과매도 상황 찾기
			overbought = [r for r in results if r.get('rsi') and r['rsi'] > 90]
			oversold = [r for r in results if r.get('rsi') and r['rsi'] < 29]
			
			if overbought:
				overbought_list = []
				for coin in overbought:
					overbought_list.append(f"{coin['symbol']}: {coin['rsi']}")
				
				message = f"🔴 과매수 신호 감지!\n" + "\n".join(overbought_list)				
				try:
					service_send_telegram_message(message)
					
					# 각 과매수 코인에 대해 숏 포지션 진입
					for coin_data in overbought:
						try:
							# 현재 내가 이 코인을 이미 가지고 있다면 포지션에 진입하지 않기
							if service_check_if_ihave_this_coin(coin_data['symbol']):
								service_send_telegram_message(f"⚠️ {coin_data['symbol']} 이미 보유 중이므로 숏 포지션 진입 건너뜀")
								continue
							
							# 현재 가격 가져오기
							klines = service_klines(coin_data['symbol'], '15m', 1)
							current_price = float(klines.iloc[-1]['Close'])
							
							# 숏 포지션 진입
							position_result = service_open_short_position(
								coin_data['symbol'],
								10,                     # 10 USDT (테스트 금액)
								5,                      # 5배 레버리지
								current_price,          # 진입가
							)
							
							# 포지션 진입 결과 확인
							if position_result and position_result.get('status') == 'success':
								entry_msg = f"📉 숏 포지션 진입 성공: {coin_data['symbol']} @ {current_price}"
								logger.info(entry_msg)
								service_send_telegram_message(entry_msg)
							else:
								error_msg = f"❌ 숏 포지션 진입 실패: {coin_data['symbol']}"
								logger.error(error_msg)
								if position_result and position_result.get('error'):
									error_detail = f"실패 원인: {position_result['error']}"
									logger.error(error_detail)
									service_send_telegram_message(f"{error_msg}\n{error_detail}")
							
						except Exception as position_error:
							logger.error(f'숏 포지션 진입 실패 {coin_data["symbol"]}: {position_error}')
					
				except Exception as telegram_error:
					logger.error(f'텔레그램 전송 실패 (과매수): {telegram_error}')
			

			if oversold:
				oversold_list = []
				for coin in oversold:
					oversold_list.append(f"{coin['symbol']}: {coin['rsi']}")
				message = f"🟢 과매도 신호 감지!\n" + "\n".join(oversold_list)				
				try:
					service_send_telegram_message(message)
										# 각 과매도 코인에 대해 롱 포지션 진입
					for coin_data in oversold:  # 루프 내부에서 처리
						try:
							# 현재 내가 이 코인을 이미 가지고 있다면 포지션에 진입하지 않기
							if service_check_if_ihave_this_coin(coin_data['symbol']):
								service_send_telegram_message(f"⚠️ {coin_data['symbol']} 이미 보유 중이므로 롱 포지션 진입 건너뜀")
								continue
							
							# 현재 가격 가져오기
							klines = service_klines(coin_data['symbol'], '15m', 1)
							current_price = float(klines.iloc[-1]['Close'])
							
							# 익절가 계산 (현재가 + 2%)
							take_profit_price = current_price * 1.02
							
							# 롱 포지션 진입
							position_result = service_open_long_position(
								coin_data['symbol'],    # coin['symbol'] → coin_data['symbol']
								10,                     # 10 USDT (테스트 금액)
								5,                      # 5배 레버리지 (안전한 레버리지)
								current_price,          # coin['price'] → current_price
							)
							
							# 포지션 진입 결과 확인
							if position_result and position_result.get('status') == 'success':
								entry_msg = f"✅ 롱 포지션 진입 성공: {coin_data['symbol']} @ {current_price}"
								service_send_telegram_message(entry_msg)
							else:
								error_msg = f"❌ 롱 포지션 진입 실패: {coin_data['symbol']}"
								logger.error(error_msg)
								if position_result and position_result.get('error'):
									error_detail = f"실패 원인: {position_result['error']}"
									logger.error(error_detail)
									service_send_telegram_message(f"{error_msg}\n{error_detail}")
							
						except Exception as position_error:
							logger.error(f'포지션 진입 실패 {coin_data["symbol"]}: {position_error}')
					
				except Exception as telegram_error:
					logger.error(f'텔레그램 전송 실패 (과매도): {telegram_error}')
				
		except Exception as e:
			logger.error(f'RSI check error: {e}')

	# 새로 추가: 1시간마다 생존 확인 메시지
	# @scheduler.scheduled_job('interval', hours=1, name='heartbeat', id='heartbeat')
	# def send_heartbeat():
	# 	try:
	# 		current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	# 		message = f"💚 살아있어요! ({current_time})"
	# 		logger.info(message)
	# 		service_send_telegram_message(message)
	# 	except Exception as e:
	# 		logger.error(f'Heartbeat error: {e}')

	scheduler.start()
	logger.info("✅ Scheduler started!")