from django.contrib.auth import get_user_model
from django.contrib.gis.db import models


class Farmer(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='farmers')
    pin_inn = models.CharField(max_length=14)
    mobile = models.CharField(max_length=20)
