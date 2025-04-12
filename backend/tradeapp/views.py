from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import logging
import traceback
from http import HTTPStatus
from django.shortcuts import render
from django.db import DatabaseError, transaction, close_old_connections
from django.shortcuts import get_object_or_404
import json
from django.db.models import Q

from tradeapp.services import *

logger = logging.getLogger('tradeapp.views')

@api_view(['GET'])
def send_telegram_message(request):
	'''
	  service_send_telegram_message가 동작하는지 테스트 하기 위한 view
	'''
	try:
		service_send_telegram_message('안녕하세요!')
		return Response(True, status=HTTPStatus.OK)
	except Exception as e:
		logger.error(f'tsend_telegram_message_get_error : {e}')
		logger.error(traceback.format_exc())
		return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
	finally:
		close_old_connections()

@api_view(['GET'])
def get_futures_wallet_balances(request):
	'''
		내가 가지고 있는 코인 배열로 보기
	'''
	if request.method == 'GET':
		try:
			result = service_get_futures_wallet_balances()
			print(result)
			return Response(result, status=HTTPStatus.OK)
		except Exception as e:
			logger.error(f'tsend_telegram_message_get_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()


@api_view(['GET'])
def get_balnace_usdt(request):
	'''
		내가가진 모든돈. 포지션에 들어있는 것도 포함됨.
	'''
	if request.method == 'GET':
		try:
			result = service_get_balnace_usdt()
			print(result)
			return Response(result, status=HTTPStatus.OK)
		except Exception as e:
			logger.error(f'tsend_telegram_message_get_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()


@api_view(['GET'])
def get_available_balance_usdt(request):
	'''
		내가가진 모든돈. 포지션에 들어있는 것은 제외. 
		예시: 54.58289113
	'''
	if request.method == 'GET':
		try:
			result = service_get_available_balance_usdt()
			print(type(result))
			return Response(result, status=HTTPStatus.OK)
		except Exception as e:
			logger.error(f'tsend_telegram_message_get_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()


@api_view(['GET'])
def get_tickers_usdt(request):
	if request.method == 'GET':
		try:
			result = service_get_tickers_usdt()
			print(result)
			return Response(result, status=HTTPStatus.OK)
		except Exception as e:
			logger.error(f'tsend_telegram_message_get_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()



@api_view(['GET'])
def get_top_ten_coins(request):
	if request.method == 'GET':
		try:
			result = service_get_top_ten_coins()
			print(result)
			return Response(result, status=HTTPStatus.OK)
		except Exception as e:
			logger.error(f'tsend_telegram_message_get_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()


@api_view(['GET'])
def klines(request):
	if request.method == 'GET':
		try:
			symbol='BTCUSDT' # 이거 설정해야함!
			result = service_klines(symbol, '15m', 10)
			# 가능한 옵션: 3m 5m 15m 1h 4h 6h 24h
			print(result)
			return Response(result, status=HTTPStatus.OK)
		except Exception as e:
			logger.error(f'tsend_telegram_message_get_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()


@api_view(['GET'])
def check_if_ihave_this_coin(request):
	'''
		내가 가지고 있는 코인인지 확인하는 서비스
	'''
	if request.method == 'GET':
		try:
			symbol='BNBUSDT' # 이거 설정해야함!
			result = service_check_if_ihave_this_coin(symbol)
			print(result)
			return Response(result, status=HTTPStatus.OK)
		except Exception as e:
			logger.error(f'tsend_telegram_message_get_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()


@api_view(['GET'])
def volume_of_avg_and_previous(request):
	if request.method == 'GET':
		try:
			symbol='BNBUSDT' # 이거 설정해야함!
			interval='15m'
			result = service_volume_of_avg_and_previous(symbol, interval)
			print(result)
			return Response(result, status=HTTPStatus.OK)
		except Exception as e:
			logger.error(f'tsend_telegram_message_get_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()


@api_view(['GET'])
def is_current_status_rising(request):
	if request.method == 'GET':
		try:
			symbol='BNBUSDT' # 이거 설정해야함!
			interval='1h'
			result = service_is_current_status_rising(symbol, interval)
			print(result)
			return Response(result, status=HTTPStatus.OK)
		except Exception as e:
			logger.error(f'tsend_telegram_message_get_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()


@api_view(['GET'])
def is_current_status_declining(request):
	if request.method == 'GET':
		try:
			symbol='BNBUSDT' # 이거 설정해야함!
			interval='1h'
			result = service_is_current_status_declining(symbol, interval)
			print(result)
			return Response(result, status=HTTPStatus.OK)
		except Exception as e:
			logger.error(f'tsend_telegram_message_get_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()

@api_view(['GET'])
def check_continuous_decline_and_sum_threshold(request):
	if request.method == 'GET':
		try:
			symbol='XRPUSDT' # 이거 설정해야함!
			interval='15m'
			result = service_check_continuous_decline_and_sum_threshold(symbol, interval)
			print(result)
			return Response(result, status=HTTPStatus.OK)
		except Exception as e:
			logger.error(f'tsend_telegram_message_get_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()

@api_view(['GET'])
def check_continuous_increase_and_sum_threshold(request):
	if request.method == 'GET':
		try:
			symbol='XTZUSDT' # 이거 설정해야함!
			interval='15m'
			result = service_check_continuous_increase_and_sum_threshold(symbol, interval)
			print(result)
			return Response(result, status=HTTPStatus.OK)
		except Exception as e:
			logger.error(f'tsend_telegram_message_get_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()

# @api_view(['GET'])
# def open_order_long(request):
# 	if request.method == 'GET':
# 		try:
# 			symbol='BNBUSDT' # 이거 설정해야함!
# 			qty=12
# 			object_sell_price=12222
# 			result = service_open_order_long(symbol, qty, object_sell_price)
# 			print(result)
# 			return Response(result, status=HTTPStatus.OK)
# 		except Exception as e:
# 			logger.error(f'tsend_telegram_message_get_error : {e}')
# 			logger.error(traceback.format_exc())
# 			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
# 		finally:
# 			close_old_connections()

@api_view(['GET'])
def get_rsi(request):
	'''
		특정 코인의 RSI 값을 반환하는 API
		기본 설정: symbol='BTCUSDT', interval='15m'
	'''
	if request.method == 'GET':
		try:
			symbol = request.GET.get('symbol', 'BTCUSDT')  # 쿼리 파라미터로 받을 수 있음
			interval = request.GET.get('interval', '15m')  # 기본값 15분

			result = service_get_rsi(symbol, interval)
			print(result)
			return Response(result, status=HTTPStatus.OK)

		except Exception as e:
			logger.error(f'get_rsi_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()