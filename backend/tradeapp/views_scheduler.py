import logging
import traceback
import time
from tradeapp.models import BuyHistory
from tradeapp.services import does_down_tail_has_long_than_top, does_top_tail_has_long_than_down, get_current_price, say_hi, service_check_if_ihave_this_coin, service_get_available_balance_usdt, service_get_tickers_usdt, get_my_favorite_coins_from_service, service_is_current_status_declining, service_is_current_status_rising, service_open_long_position, service_open_short_position, service_send_telegram_message
from django.db import close_old_connections

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
    try:
        mymoney=service_get_available_balance_usdt()
        if mymoney < 12: #내가 가진 돈이 12usd이하이면 아래 코드가 실행되지 않음
           
            logger.info('12usd이하에요 안살꺼에요.')
            return
        
        # for coin in service_get_top_ten_coins():
        for coin in service_get_tickers_usdt():
            print(coin)

            if_ihave_this_coin = service_check_if_ihave_this_coin(coin)
            if if_ihave_this_coin:
                continue  # 현재 코인을 이미 가지고 있으면 다음 코인으로 넘어감

            # print('시나리오1, # 내리는 추세에서 올랐을 때 숏에 배팅하는 시나리오.')
            is_macd_declining = service_is_current_status_declining(coin, '15m')[0] # 이평선이 음인지
            is_successing_rising = service_check_continuous_increase_and_sum_threshold(coin, '15m')
            successing_rising = is_successing_rising[0] # 연속해서 오르는가
            more_than_two_percent_short = is_successing_rising[1] # 오른게 1% 이상인가
            goal_price_short = is_successing_rising[2] # 목표가
            current_price = get_current_price(coin)
            is_successing_rising_result = successing_rising and more_than_two_percent_short # 위에조건을 둘다 만족하는가
            does_top_tail = does_top_tail_has_long_than_down(coin, '15m')
            # 이전 3개 캔들의 윗꼬리가 아래꼬리보다 긴가

            if is_macd_declining and is_successing_rising_result and does_top_tail and current_price > goal_price_short:
                service_send_telegram_message(f'{coin} 숏 거세요')
                BuyHistory.objects.create(
                    coin=coin,
                    position='short',
                    amount_usdt=12,
                    goal_price_short=goal_price_short,
                    current_price=current_price
                )
                print(coin, '이거숏 거세요')
                service_open_short_position(coin, 12, 10, current_price, goal_price_short)

            logger.info(f'is_macd_declining {is_macd_declining}')
            logger.info(f'is_successing_rising_result {is_successing_rising_result}')
            logger.info(f'does_top_tail {does_top_tail}')
            logger.info(f'current_price {current_price}')
            logger.info(f'goal_price_short {goal_price_short}')

            # print('시나리오1, # 오르는 추세에서 내렸을 때 롱에 배팅하는 시나리오.')
            is_macd_rising = service_is_current_status_rising(coin, '15m')[0] # 이평선이 양인지
            is_successing_declining = service_check_continuous_decline_and_sum_threshold(coin, '15m')
            successing_declining = is_successing_declining[0] # 연속해서 내리는가
            more_than_two_percent_long = is_successing_declining[1] # 내린게 1% 이상인가
            goal_price_long = is_successing_declining[2] # 목표가
            current_price = get_current_price(coin) 
            is_successing_declining_result = successing_declining and more_than_two_percent_long # 위에조건을 둘다 만족하는가
            does_down_tail = does_down_tail_has_long_than_top(coin, '15m') # 이전 3개 캔들의 아래꼬리가 윗꼬리보다 긴가

            if is_macd_rising and is_successing_declining_result and does_down_tail and current_price < goal_price_long:
                service_send_telegram_message(f'{coin} 롱 거세요')
                BuyHistory.objects.create(
                    coin=coin,
                    position='long', 
                    amount_usdt=12,
                    goal_price_short=goal_price_long,
                    current_price=current_price
                )
                service_open_long_position(coin, 12, 10, current_price, goal_price_short)

            logger.info(f'is_macd_rising {is_macd_rising}')
            logger.info(f'is_successing_declining_result {is_successing_declining_result}')
            logger.info(f'does_down_tail {does_down_tail}')
            logger.info(f'current_price {current_price}')
            logger.info(f'goal_price_long {goal_price_long}')

            time.sleep(1)

    except Exception as e:
        print(f'Error in scenario1: {e}')
        logger.error(f'Error in scenario1: {e}')
        logger.error(traceback.format_exc())
    finally:
        close_old_connections()

def scenario1_sell():
    print('sell')
    pass