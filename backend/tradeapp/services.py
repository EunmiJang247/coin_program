from decouple import config
import telegram
import asyncio

'''
현재 비트코인 가격 가져오는 함수: get_current_price

'''

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID')

def say_hi():
	print('hi')

def service_send_telegram_message(message):
	telegram_bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
	asyncio.run(telegram_bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text=message))