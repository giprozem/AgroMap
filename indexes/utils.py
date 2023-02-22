import matplotlib.pyplot as plt

from culture_model.models import VegetationIndex
from gip.models import ContourYear
from indexes.models import ActualVegIndex, IndexCreatingReport


def creating_indexes(date, satellite_image_id):
    for contour in range(1, (ContourYear.objects.all().count() + 1)):
        for index in range(1, (VegetationIndex.objects.all().count() + 1)):
            try:
                ActualVegIndex.objects.create(contour_id=contour, index_id=index, date=date)
                IndexCreatingReport.objects.create(
                    contour_id=contour,
                    veg_index_id=index,
                    satellite_image_id=satellite_image_id,
                    is_processed=True,
                    process_error='No error'
                )
            except Exception as e:
                IndexCreatingReport.objects.create(
                    contour_id=contour,
                    veg_index_id=index,
                    satellite_image_id=satellite_image_id,
                    is_processed=False,
                    process_error=e
                )
                plt.close()
                pass
