from django.contrib.gis.db import models

from gip.models import District
from gip.models.base import BaseModel

# TODO Translation required


class Classes(BaseModel):
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'name',
            'description'
        )


class Subclass(BaseModel):
    classes = models.ForeignKey(Classes, on_delete=models.SET_NULL, null=True, related_name='subclasses')
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'name',
            'description',
            'classes',
        )


class GroupType(BaseModel):
    subclass = models.ForeignKey(Subclass, on_delete=models.SET_NULL, null=True, related_name='group_type')
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'name',
            'description',
            'subclass',
        )


class RepublicanType(BaseModel):
    type_group = models.ForeignKey(GroupType, on_delete=models.SET_NULL, null=True, related_name='republican_type')
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'name',
            'description',
            'type_group',
        )


class DistrictType(BaseModel):
    type_group = models.ForeignKey(RepublicanType, on_delete=models.SET_NULL, null=True, related_name='district_type')
    name = models.CharField(max_length=20)
    description = models.TextField()
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'type_group',
            'name',
            'description',
            'district'
        )


class PastureCulture(BaseModel):
    district_type = models.ForeignKey(District, on_delete=models.SET_NULL, related_name='pasture_culture', null=True)
    name = models.CharField(max_length=255)
    coefficient_to_productivity = models.DecimalField(max_digits=4, decimal_places=2)
    content_of_feed = models.DecimalField(max_digits=4, decimal_places=2)
    
    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'district_type',
            'name',
            'coefficient_to_productivity',
            'content_of_feed'
        )
