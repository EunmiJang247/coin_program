import ta.trend
from decouple import config
from binance.um_futures import UMFutures
import telegram
import asyncio
from binance.error import ClientError
import pandas as pd

'''
텔레그램 메세지 보내는 함수: service_send_telegram_message
현재 비트코인 가격 가져오는 함수: get_current_price
내가가진 모든돈. 포지션에 들어있는 것은 제외. service_get_available_balance_usdt
가지고 있는 선물 포지션 배열로 주는 함수: get_futures_wallet_balances
USDT를 기준으로 거래되는 모든 암호화폐의 종류를 배열로 출력: service_get_tickers_usdt
탑탠 코인: service_get_top_ten_coins
캔들가격: service_klines
volume_of_avg_and_previous: 100개의 거래량 평균과 현재 캔들의 거래량 반환
이평선의 기울기가 14개, 21개 모두 양인지: service_is_current_status_rising
내가 이 코인을 가지고있는지 반환 bool(True/False) service_check_if_ihave_this_coin
'''

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID')
API = config('API')
SECRET = config('SECRET')
client = UMFutures(key = API, secret = SECRET)

def say_hi():
	print('hi')

def get_current_price(coin):
    price = float(client.ticker_price(coin)['price'])
    return price

def service_send_telegram_message(message):
	'''
	message에 담긴 변수를 텔레그램으로 보내줌
	'''
	telegram_bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
	asyncio.run(telegram_bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text=message))

def set_leverage(symbol, level):
  # 레버리지 설정
  try:
      client.change_leverage(
          symbol=symbol, leverage=level, recvWindow=6000
      )
  except ClientError as error:
      print(
          "4 Found error. status: {}, error code: {}, error message: {}".format(
              error.status_code, error.error_code, error.error_message
          )
      )

def set_margin_type(symbol, type):
  # 마진타입 설정 (아이솔레이티드 아니면 크로스)
  try:
      client.change_margin_type(
          symbol=symbol, marginType=type, recvWindow=6000
      )
  except ClientError as error:
      print(
          "5 Found error. status: {}, error code: {}, error message: {}".format(
              error.status_code, error.error_code, error.error_message
          )
      )
  
def service_get_futures_wallet_balances():
  '''
  가지고 있는 선물 포지션들
  결과 예시:
  [{
  'symbol': 'BTCUSDT', 
  'positionAmt': '-0.002', 현재 보유한 자산의 양
  'entryPrice': '66351.2', 포지션을 진입 또는 개장한 가격
  'breakEvenPrice': '66318.0244', 손익분기점 가격으로, 수수료 및 기타 비용을 고려한 포지션의 수익 손실이 발생하지 않는 가격
  'markPrice': '66351.10000000', 현재 시장 가격
  'unRealizedProfit': '0.00020000', 실현되지 않은 이익
  'liquidationPrice': '72670.46254980', 청산 가격
  'leverage': '10', 레버리지 수준
  'maxNotionalValue': '230000000', 최대 허용 가능한 명목 가치
  'marginType': 'isolated', 마진 유형
  'isolatedMargin': '13.22008880', 격리된 마진의 양
  'isAutoAddMargin': 'false', 자동 마진 추가 설정
  'positionSide': 'BOTH', 포지션의 방향
  'notional': '-132.70220000', 포지션의 명목 가치
  'isolatedWallet': '13.21988880', 격리된 지갑의 잔고
  'updateTime': 1721440858926, 데이터가 업데이트된 시간
  'isolated': True, 격리된 마진을 사용 중
  'adlQuantile': 2 ADL(자동 청산 메커니즘)의 분위수
  }]
  '''
  try:
      resp = client.get_position_risk() # 보유 중인 각 포지션에 대한 정보를 반환
      positions = []
      for elem in resp:
          if float(elem['positionAmt']) != 0:
              positions.append(elem)
      return positions
  except ClientError as error:
      print(
          "9 Found error. status: {}, error code: {}, error message: {}".format(
              error.status_code, error.error_code, error.error_message
          )
      )

def service_get_balnace_usdt():
    '''
    내가가진 모든돈. 포지션에 들어있는 것도 포함됨.
    예시: 67.57379794
    '''
    try:
        response = client.balance(recvWindow=6000)
        for elem in response:
            if elem['asset'] == 'USDT':
                return float(elem['balance'])
    except ClientError as error:
        print(
            "1 Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )

def service_get_available_balance_usdt():
    '''
    내가가진 모든돈. 포지션에 들어있는 것은 제외. 
    예시: 54.58289113
    '''
    try:
        response = client.balance(recvWindow=6000)
        for elem in response:
            if elem['asset'] == 'USDT':
                return float(elem['availableBalance'])
    except ClientError as error:
        print(
            "2 Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )

def service_get_tickers_usdt():
    '''
    USDT를 기준으로 거래되는 모든 암호화폐의 종류를 배열로 출력.
    [
    "TONUSDT",
    "OMGUSDT",....
    '''
    tickers = []
    resp = client.ticker_price()
    for elem in resp:
        if 'USDT' in elem['symbol']:
            tickers.append(elem['symbol'])
    return tickers


def service_get_top_ten_coins():
    tickers = ['BTCUSDT', 'BNBUSDT', 'ETHUSDT', 'BCHUSDT', 'XRPUSDT', 'EOSUSDT', 'LTCUSDT', 'TRXUSDT', 'ADAUSDT', 'ONTUSDT', 'IOTAUSDT', 'BATUSDT', 'XLMUSDT', 'XMRUSDT', 'ZECUSDT', 'ATOMUSDT', 'VETUSDT']
    # tickers = ['BTCUSDT']
    return tickers


def service_klines(symbol, interval, limit):
    '''
    심볼에 대한 최근 20개의 15분 간격 Kline 데이터
    매개변수: 심볼이름, 인터벌 ,몇개캔들

    예시:
    Time                 Open     High      Low    Close    Volume
    2024-07-19 23:30:00  66719.6  66719.6  66590.9  66613.2  1218.794
    2024-07-19 23:45:00  66613.2  66706.5  66601.0  66627.9   964.857 ...
    '''
    try:
        resp = pd.DataFrame(client.klines(symbol, interval, limit=limit))
        resp = resp.iloc[:,:6]
        resp.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'] #첫 번째 열부터 6번째 열까지 선택
        resp = resp.set_index('Time')
        resp.index = pd.to_datetime(resp.index, unit='ms')
        resp = resp.astype(float)
        return resp
    except ClientError as error:
        print("3 Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message))
        
def get_price_precision(symbol):
  # 암호화폐(symbol)의 가격 소수점 자릿수를 가져오는 함수
  resp = client.exchange_info()['symbols']
  for elem in resp:
      if elem['symbol'] == symbol:
          return elem['pricePrecision']
        

def get_qty_precision(symbol):
  # 암호화폐(symbol)의 개수 소수점 자릿수를 가져오는 함수
  resp = client.exchange_info()['symbols']
  for elem in resp:
      if elem['symbol'] == symbol:
          return elem['quantityPrecision']
      
def service_check_if_ihave_this_coin(coin):
  '''
  매개변수: coin
  내가 이 코인을 가지고있는지 반환 bool(True/False) 
  '''
  try:
      resp = client.get_position_risk() # 보유 중인 각 포지션에 대한 정보를 반환
      positions = []
      for elem in resp:
          if float(elem['positionAmt']) != 0:
              positions.append(elem['symbol'])
      return coin in positions
  except ClientError as error:
      print(
          "9 Found error. status: {}, error code: {}, error message: {}".format(
              error.status_code, error.error_code, error.error_message
          )
      )


def service_volume_of_avg_and_previous(symbol, interval):
  '''
  100개의 거래량 평균과 현재 캔들의 거래량 반환

  Parameters:
    symbol (str): 거래 쌍 심볼

  Returns:
    tuple: (직전 캔들의 거래량, 평균 거래량)
    만약 데이터를 가져오는 과정에서 오류가 발생하면 (None, None)을 반환

  반환 예시:
  평균, 현재 순서.
  [573.36,907.1138383838385]
  '''
  try:
    # 최근 100개의 Kline 데이터 가져오기
    resp = pd.DataFrame(client.klines(symbol, interval, limit=100))
    resp = resp.iloc[:,:6]
    resp.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'] # 열 이름 설정
    resp = resp.set_index('Time')
    resp.index = pd.to_datetime(resp.index, unit='ms')
    resp = resp.astype(float)

    # 현재 캔들의 거래량 구하기 (가장 최근 데이터)
    previous_volume = resp.iloc[-2]['Volume']
    avg_volume = resp.iloc[:-1]['Volume'].mean()

    # 직전 캔들의 거래량과 평균 거래량을 반환
    return avg_volume, previous_volume
  except ClientError as error:
    print("Error: {}".format(error))


def _calculate_slope(data, period):
  # 기울기를 일반적인 방식으로 계산하는 함수
  first_value = data.iloc[-period]
  last_value = data.iloc[-1]

  # 기울기 계산
  slope = (last_value - first_value) / period
  return slope


def _check_current_position_rising(coin_info_30):
  '''
  지금 상승추세인지 확인하는 함수
  '''
  ma_21_slope = _calculate_slope(coin_info_30.Close, 21)
  ma_14_slope = _calculate_slope(coin_info_30.Close, 14)
  ma_7_slope = _calculate_slope(coin_info_30.Close, 7)
  return (ma_21_slope, ma_14_slope, ma_7_slope)

def _check_current_position_declining(coin_info_40):
    '''
    지금 하락추세인지 확인하는 함수
    '''
    ma_21_slope = _calculate_slope(coin_info_40.Close, 21)
    ma_14_slope = _calculate_slope(coin_info_40.Close, 14)
    ma_7_slope = _calculate_slope(coin_info_40.Close, 7)
    return (ma_21_slope, ma_14_slope, ma_7_slope)

def service_is_current_status_rising(coin, interval):
  '''
  매개변수: 코인이름, 인터벌
  이평선의 기울기가 14개, 21개 모두 양인지 

  결과예시: 
  [
    false,
    -0.1954999999999984,
    -0.04923076923076818,
    0.5800000000000031
  ]
  '''
  ma_21_slope, ma_14_slope, ma_7_slope = _check_current_position_rising(service_klines(coin, interval, 30))
  if ma_14_slope > 0 and ma_21_slope > 0 :
      return (True, ma_21_slope, ma_14_slope, ma_7_slope)
  else:
      return (False, ma_21_slope, ma_14_slope, ma_7_slope)


def service_is_current_status_declining(coin, interval):
  '''
  매개변수: 코인이름, 인터벌
  이평선의 기울기가 14개, 21개 모두 음인지 

  결과예시: 
  [
    false,
    -0.1954999999999984,
    -0.04923076923076818,
    0.5800000000000031
  ]
  '''
  ma_21_slope, ma_14_slope, ma_7_slope = _check_current_position_declining(service_klines(coin, interval, 30))
  if ma_14_slope < 0 and ma_21_slope < 0 :
      return (True, ma_21_slope, ma_14_slope, ma_7_slope)
  else:
      return (False, ma_21_slope, ma_14_slope, ma_7_slope)


def service_check_continuous_decline_and_sum_threshold(coin, interval):
  '''
  상승 추세에서 최근 4캔들 중에서 가격이 연속해서 내려갔고, 내려간 가격의 합이 처음 가격의 1% 이상인지 확인하는 함수
  
  Parameters:
  코인, 인터벌
  
  Returns:
  bool: 최근 4개 캔들 중에서 가격이 연속해서 내려갔고, 내려간 가격의 합이 처음 가격의 1% 이상이면 True, 아니면 False, 목표가(이가격에 팔겠다), 내려간 비율
  '''
  try:
    # 최근 4개 캔들의 Close 가격 데이터를 가져옴
    coin_info=service_klines(coin, interval, 5)
    # print(coin_info)
    # print(coin_info.iloc[0]['Open']) # 1시간 전
    # print(coin_info.iloc[1]) # 45분전
    # print(coin_info.iloc[2]) # 30분전
    # print(coin_info.iloc[3]) # 15분전
    # print(coin_info.iloc[4]) # 현재 
    # print(coin_info.iloc[-1]) # 현재

    is_continuous_decline = True
    for i in range(1, 4):
    #   1,2,3을 순회함
      if coin_info.iloc[i]['Open'] <= coin_info.iloc[i]['Close']:  # 이전 캔들보다 가격이 같거나 높으면
        is_continuous_decline = False
    
    # 내려간 가격의 합이 처음 가격의 1% 이상인지 확인
    decline_sum = coin_info.iloc[0]['Open'] - coin_info.iloc[-1]['Close']  # 내려간 가격의 합
    decline_threshold = coin_info.iloc[0]['Open'] * 0.005
    percentage = round((decline_sum / coin_info.iloc[0]['Open']) * 100, 2) # 내린 퍼센트
    
    return is_continuous_decline, decline_sum >= decline_threshold, coin_info.iloc[3]['Open'], percentage
  
  except Exception as e:
    print(f"Error in check_continuous_decline_and_sum_threshold: {e}")
    return False


def service_check_continuous_increase_and_sum_threshold(coin, interval):
  '''
  하락추세에서 최근 4캔들 중에서 가격이 연속해서 올라갔고, 올라간 가격의 합이 처음 가격의 1% 이상인지 확인하는 함수
  
  Parameters:
  coin_info (DataFrame): 코인 정보가 담긴 데이터프레임. 최소 4개의 캔들 데이터를 포함해야 함.
  
  Returns:
  bool: 최근 4개 캔들 중에서 가격이 연속해서 올라갔고, 올라간 가격의 합이 처음 가격의 1% 이상이면 True, 아니면 False, 처음값, 마지막값, 올라간 비율
  '''
  try:
    coin_info = service_klines(coin, interval, 5)
    # print(coin_info)
    # print(coin_info.iloc[0]['Open']) # 1시간 전
    # print(coin_info.iloc[1]) # 45분전
    # print(coin_info.iloc[2]) # 30분전
    # print(coin_info.iloc[3]) # 15분전
    # print(coin_info.iloc[4]) # 현재 
    # print(coin_info.iloc[-1]) # 현재
    
    is_continuous_increase = True
    for i in range(1, 4):
    #   1,2,3을 순회함
      if coin_info.iloc[i]['Open'] >= coin_info.iloc[i]['Close']: 
        is_continuous_increase = False
        # print(is_continuous_increase)
    
    # 올라간 가격의 합이 처음 가격의 1% 이상인지 확인
    increase_sum = coin_info.iloc[-1]['Close'] - coin_info.iloc[0]['Open']  # 내려간 가격의 합
    increase_threshold = coin_info.iloc[0]['Open'] * 0.005
    percentage = round((increase_sum / coin_info.iloc[0]['Open']) * 100, 2)
    
    return is_continuous_increase, increase_sum >= increase_threshold, coin_info.iloc[3]['Open'], percentage
  
  except Exception as e:
    print(f"Error in check_continuous_increase_and_sum_threshold: {e}")
    return False


def does_down_tail_has_long_than_top(coin, interval):
    '''
    그래프의 3개 이전 캔들 모두 위꼬리보다 아래꼬리가 길었는지(올라갈때를 판별하는 함수)
    롱에 배팅할 경우 사용되고, 모두 음봉일 때 사용됨. 
    '''
    try:
        coin_info = service_klines(coin, interval, 5)
        does_down_tail_has_long = True
        for i in range(1, 4):
        #   1,2,3을 순회함
            # up_tail = coin_info.iloc[i]['High'] - coin_info.iloc[i]['Open']
            down_tail = coin_info.iloc[i]['Close'] - coin_info.iloc[i]['Low']
            # if up_tail >= down_tail: 
            if  down_tail == 0: 
                does_down_tail_has_long = False
        return does_down_tail_has_long

    except Exception as e:
        print(f"Error in check_continuous_increase_and_sum_threshold: {e}")
        return False


def does_top_tail_has_long_than_down(coin, interval):
    '''
    15분 그래프의 3개 이전 캔들 모두 아래꼬리보다 위꼬리가 길었는지(내려갈때를 판별하는 함수)
    숏에 배팅할 경우 사용되고, 모두 양봉일 때 사용됨. 
    '''
    try:
        coin_info = service_klines(coin, interval, 5)
        does_top_tail_has_long = True
        for i in range(1, 4):
        #   1,2,3을 순회함
            up_tail = coin_info.iloc[i]['High'] - coin_info.iloc[i]['Close']
            # down_tail = coin_info.iloc[i]['Open'] - coin_info.iloc[i]['Low']
            # if up_tail <= down_tail:
            if up_tail == 0: 
                does_top_tail_has_long = False
        return does_top_tail_has_long

    except Exception as e:
        print(f"Error in check_continuous_increase_and_sum_threshold: {e}")
        return False

def service_open_long_position(coin, usdt_amount, leverage, current_price, object_sell_price):
    qty_precision = get_qty_precision(coin)
    qty = round(float(round(usdt_amount / current_price, 6)) * leverage, qty_precision)

    try:
        client.new_order(symbol=coin, side="BUY", type='LIMIT', quantity=qty, timeInForce='GTC', price=current_price)
        client.new_order(symbol=coin, side="SELL", type='TAKE_PROFIT_MARKET', quantity=qty, timeInForce='GTC', stopPrice=object_sell_price)
    except ClientError as e:
        print(f"주문 오류 발생: {e}")


def service_open_short_position(coin, usdt_amount, leverage, current_price, object_sell_price):
    qty_precision = get_qty_precision(coin)
    qty = round(float(round(usdt_amount / current_price, 6)) * leverage, qty_precision)

    try:
        client.new_order(symbol=coin, side="SELL", type='LIMIT', quantity=qty, timeInForce='GTC', price=current_price)
        client.new_order(symbol=coin, side="BUY", type='TAKE_PROFIT_MARKET', quantity=qty, timeInForce='GTC', stopPrice=object_sell_price)
    except ClientError as e:
        print(f"주문 오류 발생: {e}")