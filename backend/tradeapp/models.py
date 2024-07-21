from django.db import models

class Coin(models.Model):
	file_name = models.CharField(max_length=100) 
	class Meta:
		db_table = 'coin_name'

class BuyHistory(models.Model):
	create_datetime = models.DateTimeField(auto_now_add=True) # 생성된 날짜와 시간
	delete_datetime = models.DateTimeField(null=True, blank=True) # 삭제된 날짜와 시간
	coin = models.CharField(max_length=50) # 코인 이름
	position = models.CharField(max_length=50) # 포지션
	amount_usdt = models.DecimalField(max_digits=15, decimal_places=4) # 구매한 USDT 금액
	goal_price_short = models.DecimalField(max_digits=15, decimal_places=4) # 목표 가격
	current_price = models.DecimalField(max_digits=15, decimal_places=4)  # 현재가격
 
	class Meta:
		db_table = 'buy_history'