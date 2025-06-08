from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
	path('send_telegram_message', send_telegram_message),
	path('get_futures_wallet_balances', get_futures_wallet_balances),
	path('get_balnace_usdt', get_balnace_usdt),
	path('get_available_balance_usdt', get_available_balance_usdt),
	path('get_tickers_usdt', get_tickers_usdt),
	path('get_top_ten_coins', get_top_ten_coins),
	path('klines', klines),
	path('check_if_ihave_this_coin', check_if_ihave_this_coin),
	path('volume_of_avg_and_previous', volume_of_avg_and_previous),
	path('is_current_status_rising', is_current_status_rising),
	path('is_current_status_declining', is_current_status_declining),
	path('check_continuous_decline_and_sum_threshold', check_continuous_decline_and_sum_threshold),
	path('check_continuous_increase_and_sum_threshold', check_continuous_increase_and_sum_threshold),
	path('get_rsi', get_rsi),
 	path('get_macd', get_macd),
]