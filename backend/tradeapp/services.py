from decouple import config

def get_current_price(coin):
  print('hi..?')
  print(config('SECRET_KEY'))