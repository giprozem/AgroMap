from concurrent.futures import ThreadPoolExecutor
from functools import partial

from gip.models.contour import Contour
from indexes.models.actual_veg_index import ActualVegIndex
from indexes.models.actual_veg_index_logs import IndexCreatingReport
from indexes.models.satelliteimage import SciHubImageDate
from indexes.utils import veg_index_creating


def run():
    """
    The script aims to process satellite images, stored in a model SciHubImageDate, in parallel.
    It uses a utility function veg_index_creating to create a vegetation index for each satellite image.
    This utility function is expected to interact with multiple models,
    including Contour, IndexCreatingReport, and ActualVegIndex.
    """
    satellite_images = SciHubImageDate.objects.all()

    veg_index_creating_preset = partial(
        veg_index_creating,
        contour_obj=Contour,
        creating_report_obj=IndexCreatingReport,
        veg_index_obj=ActualVegIndex
    )
    with ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(veg_index_creating_preset, satellite_images)
