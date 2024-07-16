from http import HTTPStatus
import logging
import traceback
from datetime import datetime
import time
import os
import uuid
from tradeapp.services import get_current_price
from rest_framework.response import Response

from django.db.models import Q, Max, F, Count, Value
from django.db import close_old_connections, connection, transaction
import requests

def check_current_price():
	try:
		get_current_price('luna')

	except Exception as e:
		print(f'check_current_price : {e}')
		# logger.error(f'camera_state_error : {e}')
		# logger.error(traceback.format_exc())
	finally:
		close_old_connections()