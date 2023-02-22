from django.contrib.gis.db import models


class IndexCreatingReport(models.Model):
    contour = models.ForeignKey('gip.ContourYear', on_delete=models.SET_NULL, null=True)
    veg_index = models.ForeignKey('culture_model.VegetationIndex', on_delete=models.SET_NULL, null=True)
    satellite_image = models.ForeignKey('indexes.SatelliteImages', on_delete=models.SET_NULL, null=True)
    is_processed = models.BooleanField(default=False)
    process_error = models.TextField()
