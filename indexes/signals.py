import time
from threading import Thread

from django.db.models.signals import post_save
from django.dispatch import receiver

from indexes.models.satelliteimage import SatelliteImages

