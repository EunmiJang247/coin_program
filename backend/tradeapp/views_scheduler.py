from http import HTTPStatus
import logging
import traceback
from datetime import datetime
import time
import os
import uuid
from tradeapp.services import get_current_price, say_hi, service_check_continuous_decline_and_sum_threshold, service_check_continuous_increase_and_sum_threshold, service_check_if_ihave_this_coin, service_get_available_balance_usdt, service_get_tickers_usdt, service_get_top_ten_coins, service_is_current_status_declining, service_is_current_status_rising, service_send_telegram_message
from rest_framework.response import Response

from django.db.models import Q, Max, F, Count, Value
from django.db import close_old_connections, connection, transaction
import requests

logger = logging.getLogger('scheduler')

def check_current_price():
	try:
		say_hi()

	except Exception as e:
		print(f'check_current_price : {e}')
		logger.error(f'camera_state_error : {e}')
		logger.error(traceback.format_exc())
	finally:
		close_old_connections()

def scenario1_buy():
	print('돈느건가..?')
	try:
		mymoney=service_get_available_balance_usdt()
		if mymoney < 12: #내가 가진 돈이 12usd이하이면 아래 코드가 실행되지 않음
			logger.info('12usd이하에요 안살꺼에요.')
			return
		
		# for coin in service_get_top_ten_coins():
		for coin in service_get_tickers_usdt():
			if_ihave_this_coin = service_check_if_ihave_this_coin(coin)
			if if_ihave_this_coin:
				continue  # 현재 코인을 이미 가지고 있으면 다음 코인으로 넘어감

			print('시나리오1, # 내리는 추세에서 올랐을 때 숏에 배팅하는 시나리오.')
			is_macd_declining = service_is_current_status_declining(coin, '15m')[0] # 이평선이 음인지
			is_successing_rising = service_check_continuous_increase_and_sum_threshold(coin, '15m')
			successing_rising = is_successing_rising[0] # 연속해서 오르는가
			more_than_two_percent_short = is_successing_rising[1] # 오른게 1% 이상인가
			goal_price_short = is_successing_rising[2] # 목표가
			current_price = get_current_price(coin)
			is_successing_rising_result = successing_rising and more_than_two_percent_short # 위에조건을 둘다 만족하는가

			if is_macd_declining and is_successing_rising_result:
				# 현재가격이 목표가보다 낮을 때 라는 조건 추가 필요! and current_price > goal_price_short
				service_send_telegram_message(f'{coin} 숏 거세요')
				print(coin, '이거숏 거세요')

			print('시나리오1, # 오르는 추세에서 내렸을 때 롱에 배팅하는 시나리오.')
			is_macd_rising = service_is_current_status_rising(coin, '15m')[0] # 이평선이 양인지
			is_successing_declining = service_check_continuous_decline_and_sum_threshold(coin, '15m')
			successing_declining = is_successing_declining[0] # 연속해서 내리는가
			more_than_two_percent_long = is_successing_declining[1] # 내린게 1% 이상인가
			goal_price_long = is_successing_declining[2] # 목표가
			current_price = get_current_price(coin)
			is_successing_declining_result = successing_declining and more_than_two_percent_long # 위에조건을 둘다 만족하는가

			if is_macd_rising and is_successing_declining_result:
				# 현재가격이 목표가보다 낮을 때 라는 조건 추가 필요! and current_price < goal_price_long
				service_send_telegram_message(f'{coin} 롱 거세요')
				logger.info(coin, '이거롱 거세요')

	except Exception as e:
		print(f'Error in scenario1: {e}')
		logger.error(f'Error in scenario1: {e}')
		logger.error(traceback.format_exc())
	finally:
		close_old_connections()