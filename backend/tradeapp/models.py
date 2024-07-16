from django.db import models

class Coin(models.Model):
	file_name = models.CharField(max_length=100) 
	class Meta:
		db_table = 'coin_name'
