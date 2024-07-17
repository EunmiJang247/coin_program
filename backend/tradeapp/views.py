from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import logging
import traceback
from http import HTTPStatus
from django.shortcuts import render
from django.db import DatabaseError, transaction, close_old_connections
from django.shortcuts import get_object_or_404
import json
from django.db.models import Q

from tradeapp.services import *

logger = logging.getLogger('tradeapp.views')

@api_view(['GET'])
def send_telegram_message(request):
	if request.method == 'GET':
		try:
			service_send_telegram_message('안녕하세요!')
			return Response(True, status=HTTPStatus.OK)
		except Exception as e:
			logger.error(f'tsend_telegram_message_get_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()