import math
from time import time
from decouple import config
from binance.um_futures import UMFutures
import telegram
import asyncio
from binance.error import ClientError
import pandas as pd
import numpy as np

'''
    가지고 있는 선물 포지션들 service_get_futures_wallet_balances
    내가가진 모든돈. 포지션에 들어있는 것은 제외. service_get_available_balance_usdt
    가지고 있는 선물 포지션 배열로 주는 함수: get_futures_wallet_balances
    USDT를 기준으로 거래되는 모든 암호화폐의 종류를 배열로 출력: service_get_tickers_usdt
    탑탠 코인: get_my_favorite_coins_from_service
    캔들가격: service_klines
    volume_of_avg_and_previous: 100개의 거래량 평균과 현재 캔들의 거래량 반환
    이평선의 기울기가 14개, 21개 모두 양인지: service_is_current_status_rising
    내가 이 코인을 가지고있는지 반환 bool(True/False) service_check_if_ihave_this_coin
    숏포지션 진입 service_open_short_position
    롱포지션 진입 service_open_long_position
'''

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID')
API = config('API')
SECRET = config('SECRET')
client = UMFutures(key = API, secret = SECRET)

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
        }, ]
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


def get_my_favorite_coins_from_service():
    tickers = [
    "BTCUSDT",
    "BNBUSDT",
    "ETHUSDT",
    "BCHUSDT"
    "XRPUSDT",
    "LTCUSDT",
    "TRXUSDT",
    "ETCUSDT",
    "LINKUSDT",
    "XLMUSDT",
    "ADAUSDT",
    "XMRUSDT",
    "DASHUSDT",
    "ZECUSDT",
    "XTZUSDT",
    "ATOMUSDT",
    "ONTUSDT",
    "IOTAUSDT"
    ]
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
  ''' 암호화폐(symbol)의 가격 소수점 자릿수를 가져오는 함수 '''
  resp = client.exchange_info()['symbols']
  for elem in resp:
      if elem['symbol'] == symbol:
          return elem['pricePrecision']
        

def get_qty_precision(symbol):
  ''' 암호화폐(symbol)의 개수 소수점 자릿수를 가져오는 함수 '''
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
    interval (str): 시간 간격

  Returns:
    dict: 거래량 분석 결과
    {
      "average_volume": 1234.567,      // 과거 100개 캔들의 평균 거래량
      "current_volume": 2468.123,      // 현재(최신) 캔들의 거래량
      "volume_ratio": 2.0,             // 현재/평균 비율
      "is_high_volume": true           // 평균보다 높은 거래량인지 여부
    }
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
    current_volume = resp.iloc[-1]['Volume']
    # 과거 99개 캔들의 평균 거래량 (현재 캔들 제외)
    avg_volume = resp.iloc[:-1]['Volume'].mean()
    
    # 거래량 비율 계산
    volume_ratio = round(current_volume / avg_volume, 2) if avg_volume > 0 else 0
    
    # 평균보다 높은 거래량인지 확인
    is_high_volume = current_volume > avg_volume

    return {
        "average_volume": round(avg_volume, 3),
        "current_volume": round(current_volume, 3),
        "volume_ratio": volume_ratio,
        "is_high_volume": is_high_volume
    }
    
  except ClientError as error:
    print("Error: {}".format(error))
    return {
        "error": str(error),
        "average_volume": None,
        "current_volume": None,
        "volume_ratio": None,
        "is_high_volume": None
    }

def _calculate_slope(data, period):
  '''
    기울기를 일반적인 방식으로 계산하는 함수
  '''
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
            up_tail = coin_info.iloc[i]['High'] - coin_info.iloc[i]['Open']
            down_tail = coin_info.iloc[i]['Close'] - coin_info.iloc[i]['Low']
            if up_tail >= down_tail: 
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
            down_tail = coin_info.iloc[i]['Open'] - coin_info.iloc[i]['Low']
            if up_tail <= down_tail:
                does_top_tail_has_long = False
        return does_top_tail_has_long

    except Exception as e:
        print(f"Error in check_continuous_increase_and_sum_threshold: {e}")
        return False
        
def calculate_rsi(closes, period=14):
    """
    바이낸스와 동일한 방식의 RSI 계산 (Wilder's Smoothing)
    """
    if len(closes) < period + 1:
        return None
    
    df = pd.Series(closes)
    delta = df.diff().dropna()  # NaN 값 제거
    
    # 상승분과 하락분 분리
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    
    # 첫 번째 기간의 평균 계산
    avg_gain = up.iloc[:period].mean()
    avg_loss = down.iloc[:period].mean()
    
    # 0으로 나누기 방지
    if avg_loss == 0:
        return 100.0
    
    # Wilder's smoothing 적용
    alpha = 1.0 / period
    
    gains = [avg_gain]
    losses = [avg_loss]
    
    for i in range(period, len(up)):
        gain = alpha * up.iloc[i] + (1 - alpha) * gains[-1]
        loss = alpha * down.iloc[i] + (1 - alpha) * losses[-1]
        gains.append(gain)
        losses.append(loss)
    
    # RSI 계산
    if losses[-1] == 0:
        return 100.0
    
    rs = gains[-1] / losses[-1]
    rsi = 100 - (100 / (1 + rs))
    
    # NaN 체크
    if pd.isna(rsi):
        return None
        
    return round(float(rsi), 2)

        
def service_get_rsi(symbol, interval):
    """
    symbol과 interval을 입력받아 RSI 값을 계산해 반환
    """
    try:
        # 더 많은 데이터를 가져와서 정확도 향상
        klines_df = service_klines(symbol, interval, 100)  
        
        if klines_df is None or len(klines_df) < 15:
            return {
                'symbol': symbol, 
                'interval': interval, 
                'rsi': None,
                'period': 14,
                'error': 'Insufficient data'
            }
        
        closes = klines_df['Close'].values.astype(float)
        
        # NaN 또는 무한대 값 확인
        if np.any(pd.isna(closes)) or np.any(np.isinf(closes)):
            return {
                'symbol': symbol, 
                'interval': interval, 
                'rsi': None,
                'period': 14,
                'error': 'Invalid price data'
            }
        
        rsi = calculate_rsi(closes, period=14)
        
        if rsi is None:
            return {
                'symbol': symbol, 
                'interval': interval, 
                'rsi': None,
                'period': 14,
                'error': 'RSI calculation failed'
            }

        return {
            'symbol': symbol, 
            'interval': interval, 
            'rsi': rsi,
            'period': 14
        }
    
    except Exception as e:
        print(f"Error in service_get_rsi: {e}")
        return {
            'symbol': symbol, 
            'interval': interval, 
            'rsi': None,
            'period': 14,
            'error': str(e)
        }
        
def service_get_all_favorite_coins_rsi(interval='15m'):
    """
    favorite 코인들의 RSI를 모두 계산해서 반환
    """
    favorite_coins = get_my_favorite_coins_from_service()
    results = []
    
    for coin in favorite_coins:
        try:
            rsi_data = service_get_rsi(coin, interval)
            results.append(rsi_data)
        except Exception as e:
            print(f"Error getting RSI for {coin}: {e}")
            results.append({
                'symbol': coin,
                'interval': interval,
                'rsi': None,
                'period': 14,
                'error': str(e)
            })
    
    return results

def service_open_long_position(coin, usdt_amount, leverage, current_price):
    # 레버리지와 마진 타입 설정 추가
    set_leverage(coin, leverage)
    set_margin_type(coin, 'ISOLATED')  # 또는 'CROSS'
    
    qty_precision = get_qty_precision(coin)
    qty = round(float(round(usdt_amount / current_price, 6)) * leverage, qty_precision)

    try:
        # 매수 주문 (롱 포지션 진입)
        buy_order = client.new_order(
            symbol=coin, 
            side="BUY", 
            type='LIMIT', 
            quantity=qty, 
            timeInForce='GTC', 
            price=current_price
        )
        print(f"✅ 롱 포지션 진입: {coin} {qty}개 @ {current_price}")
        
        return {
            'status': 'success',
            'buy_order': buy_order,
            'quantity': qty,
            'entry_price': current_price
        }
        
    except ClientError as e:
        error_msg = f"주문 오류 발생: {e}"
        print(error_msg)
        return {
            'status': 'error',
            'error': error_msg
        }


def service_open_short_position(coin, usdt_amount, leverage, current_price):
    """
    숏 포지션 진입 함수
    과매수 상황에서 가격 하락을 예상하여 매도 포지션 진입
    """
    try:
        # 레버리지와 마진 타입 설정
        set_leverage(coin, leverage)
        set_margin_type(coin, 'ISOLATED')  # 또는 'CROSS'
        
        qty_precision = get_qty_precision(coin)
        qty = round(float(round(usdt_amount / current_price, 6)) * leverage, qty_precision)

        # 매도 주문 (숏 포지션 진입)
        sell_order = client.new_order(
            symbol=coin, 
            side="SELL", 
            type='LIMIT', 
            quantity=qty, 
            timeInForce='GTC', 
            price=current_price
        )
        
        return {
            'status': 'success',
            'sell_order': sell_order,
            'quantity': qty,
            'entry_price': current_price,
        }
        
    except ClientError as e:
        error_msg = f"숏 포지션 오류 발생: {e}"
        print(error_msg)
        return {
            'status': 'error',
            'error': error_msg
        }


def _get_symbol_filters(client, symbol):
    """선물 exchangeInfo에서 lot stepSize, minQty, maxQty를 얻습니다."""
    info = client.futures_exchange_info()
    sym = next(s for s in info['symbols'] if s['symbol'] == symbol)
    lot = next(f for f in sym['filters'] if f['filterType'] == 'LOT_SIZE')
    step = float(lot['stepSize'])
    min_qty = float(lot['minQty'])
    max_qty = float(lot['maxQty'])
    return step, min_qty, max_qty

def _round_to_step(qty, step):
    # step의 소수자릿수에 맞춰 floor
    precision = int(round(-math.log10(step))) if step < 1 else 0
    floored = math.floor(qty / step) * step
    # 부동소수점 표시 깨짐 방지
    return float(f"{floored:.{precision}f}")

def _detect_hedge_mode(client):
    # 헷지모드 여부
    a = client.futures_account_config()
    return a.get('dualSidePosition') is True

def service_close_position(symbol, position_amt, *, max_attempts=3, sleep_sec=0.3, cancel_open_orders=False):
    """
    포지션 종료 (USDT-M 선물)
    - position_amt: +면 롱 보유, -면 숏 보유
    - 헷지모드/원웨이 모두 지원
    - 수량 라운딩 및 reduceOnly 적용
    """
    try:
        # 0 가드
        if not position_amt or abs(float(position_amt)) == 0.0:
            return {'status': 'success', 'message': f'{symbol} 이미 청산됨', 'quantity': 0}

        position_amt = float(position_amt)
        side = "SELL" if position_amt > 0 else "BUY"  # 롱 닫기=SELL, 숏 닫기=BUY
        pos_side = "LONG" if position_amt > 0 else "SHORT"

        # 헷지 모드 확인
        hedge = _detect_hedge_mode(client)

        # 필요 시 기존 주문 취소(감축/TP/SL 등)
        if cancel_open_orders:
            try:
                client.futures_cancel_all_open_orders(symbol=symbol)
            except Exception as e:
                print(f"[{symbol}] open orders cancel 실패(무시 가능): {e}")

        # 수량 라운딩
        step, min_qty, max_qty = _get_symbol_filters(client, symbol)
        target_qty = abs(position_amt)
        qty = max(min(_round_to_step(target_qty, step), max_qty), min_qty)

        if qty < min_qty:
            return {'status': 'error', 'error': f'{symbol} 최소 수량 미만: {qty} < {min_qty}'}

        last_error = None
        for attempt in range(1, max_attempts + 1):
            try:
                params = dict(
                    symbol=symbol,
                    side=side,
                    type='MARKET',
                    quantity=qty,
                    reduceOnly=True,
                    newOrderRespType='RESULT',
                )
                if hedge:
                    params['positionSide'] = pos_side  # 헷지모드 필수

                order = client.futures_create_order(**params)

                # 잔여 포지션이 남았는지 확인 → 있으면 한 번 더 시도
                # (정확한 잔여는 계좌 포지션을 다시 조회해야 함)
                try:
                    positions = client.futures_position_information(symbol=symbol)
                    # 헷지면 LONG/SHORT 각자, 원웨이면 하나만 리턴
                    remain = 0.0
                    for p in positions:
                        if hedge:
                            if p.get('positionSide') != pos_side:  # 반대쪽은 무시
                                continue
                        amt = float(p['positionAmt'])
                        # 같은 쪽의 절대 잔량만
                        if (position_amt > 0 and amt > 0) or (position_amt < 0 and amt < 0):
                            remain = abs(amt)
                            break

                    if remain <= 0:
                        print(f"✅ 포지션 종료 완료: {symbol} {qty}")
                        return {'status': 'success', 'close_order': order, 'symbol': symbol, 'quantity': qty}
                    else:
                        # 남은 양만큼 재라운딩해서 재시도
                        qty = _round_to_step(remain, step)
                        if qty < min_qty:
                            print(f"✅ 포지션 거의 0, step/minQty 때문에 잔여 무시: remain={remain}")
                            return {'status': 'success', 'close_order': order, 'symbol': symbol, 'quantity': qty, 'note': '잔여 미만'}
                        time.sleep(sleep_sec)
                        continue
                except Exception as e:
                    # 잔여 확인 실패 → 주문 자체는 보냈으니 성공으로 간주하거나 warning 처리
                    print(f"[{symbol}] 잔여 확인 실패(성공 가능): {e}")
                    return {'status': 'success', 'close_order': order, 'symbol': symbol, 'quantity': qty, 'note': '잔여 확인 실패'}

            except ClientError as ce:
                last_error = f"ClientError: {ce}"
                print(f"[{symbol}] close attempt {attempt}/{max_attempts} 실패: {ce}")
                time.sleep(sleep_sec)

        return {'status': 'error', 'error': last_error or 'unknown error'}

    except Exception as e:
        print(f"[{symbol}] 포지션 종료 오류")
        return {'status': 'error', 'error': str(e)}