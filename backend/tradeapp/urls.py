from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
	path('send_telegram_message', send_telegram_message),
	# 텔레그램 메세지 보내기  
	path('get_futures_wallet_balances', get_futures_wallet_balances),
	# 내가 가지고 있는 코인 배열로 보기
	path('get_balnace_usdt', get_balnace_usdt),
	# 내가가진 모든돈. 포지션에 들어있는 것도 포함됨.
	path('get_available_balance_usdt', get_available_balance_usdt),
	# 내가가진 모든돈. 포지션에 들어있는 것은 제외. 
	path('get_tickers_usdt', get_tickers_usdt),
	# USDT 마켓의 모든 코인 티커 정보를 반환하는 API
	path('get_my_favorite_coins', get_my_favorite_coins),
	# 내가 좋아하는 코인 티커 리스트 반환하는 API
	path('klines', klines),
	# 심볼에 대한 최근 N개의 Kline 데이터 ( Open High Low Close Volume를 줌)
	path('check_if_ihave_this_coin', check_if_ihave_this_coin),
	# 내가 가지고 있는 코인인지 확인하는 서비스
	path('volume_of_avg_and_previous', volume_of_avg_and_previous),
	# 과거 100개 캔들의 평균 거래량과 현재 캔들의 거래량 반환
	path('is_current_status_rising', is_current_status_rising),
	# 21일, 14일, 7일 이동평균의 기울기를 모두 계산하여 현재 상승추세인지 반환
	# 순서는 21 - 14 - 7
	path('is_current_status_declining', is_current_status_declining),
	# 21일, 14일, 7일 이동평균의 기울기를 모두 계산하여 현재 하락추세인지 반환
	# 순서는 21 - 14 - 7
	path('get_rsi', get_rsi)
	# RSI 지표 계산하여 반환
]