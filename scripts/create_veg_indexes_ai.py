from concurrent.futures import ThreadPoolExecutor
from functools import partial

from ai.models.predicted_contour import Contour_AI
from indexes.models import PredictedContourVegIndex, ContourAIIndexCreatingReport
from indexes.models.satelliteimage import SciHubImageDate
from indexes.utils import veg_index_creating


def run():
    satellite_images = SciHubImageDate.objects.all()

    veg_index_creating_preset = partial(
        veg_index_creating,
        contour_obj=Contour_AI,
        creating_report_obj=ContourAIIndexCreatingReport,
        veg_index_obj=PredictedContourVegIndex
    )
    with ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(veg_index_creating_preset, satellite_images)
