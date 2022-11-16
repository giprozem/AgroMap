from django.contrib.auth import get_user_model
from django.contrib.gis.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

    class Meta:
        abstract = True
