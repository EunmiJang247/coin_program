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

logger = logging.getLogger('cameraapp.views')

@api_view(['GET'])
def boilerplate(request):
	if request.method == 'GET':
		try:
			print('hi')
			return Response('hi', status=HTTPStatus.OK)
		except Exception as e:
			logger.error(f'group_list_get_error : {e}')
			logger.error(traceback.format_exc())
			return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			close_old_connections()