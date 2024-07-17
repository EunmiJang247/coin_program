import uuid
import logging
import cv2
import time
import os
import traceback
from rest_framework import serializers
from django.db.models import Q, Max, F, Count
from django.db.models.functions import Coalesce
from django.core.files.storage import FileSystemStorage
from .models import *

logger = logging.getLogger('cameraapp.serializers')
VISIBLE_WIDTH = 1000

class CameraGroupSerializer(serializers.ModelSerializer):
	class Meta:
		pass