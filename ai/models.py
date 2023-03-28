from django.contrib.gis.db import models


class Images(models.Model):
    image = models.ImageField(upload_to='media/', blank=True)


class Canton(models.Model):
    name = models.CharField(max_length=50, blank=True)


class Contour(models.Model):
    polygon = models.GeometryField(geography='Kyrgyzstan', blank=True, null=True)
    conf = models.FloatField(null=True)
    culture = models.CharField(max_length=50, blank=True)
    image = models.ForeignKey(Images, on_delete=models.PROTECT, related_name='images')
    canton = models.ForeignKey(Canton, on_delete=models.PROTECT, related_name='canton')
    productivity = models.CharField(max_length=20, blank=True)


class Yolo(models.Model):
    ai = models.FileField(upload_to='models/')
