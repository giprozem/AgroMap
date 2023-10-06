from gip.models.contour import Contour
from indexes.models.actual_veg_index import ActualVegIndex
from indexes.models.actual_veg_index_logs import IndexCreatingReport
from indexes.models.satelliteimage import SciHubImageDate
from indexes.utils import veg_index_creating
import time
from functools import partial
from concurrent.futures import ThreadPoolExecutor


def run():
    """
    The script aims to process satellite images, stored in a model SciHubImageDate, in parallel.
    It uses a utility function veg_index_creating to create a vegetation index for each satellite image.
    This utility function is expected to interact with multiple models,
    including Contour, IndexCreatingReport, and ActualVegIndex.
    """

    # Record the start time for measuring elapsed time
    start_time = time.time()

    # Retrieve distinct years from the Contour model
    years = set(Contour.objects.values_list('year', flat=True).order_by('-year').distinct())

    # Iterate over each retrieved year
    for year in years:
        print(year)

        # Fetch contours associated with the current year, ordered by their ID
        contours = Contour.objects.filter(year=year).order_by('id')

        # For each contour, process satellite images corresponding to the current year
        for contour in contours:
            satellite_images = SciHubImageDate.objects.filter(date__year=year)

            # Define a partial function to handle creation of vegetation index for each satellite image
            veg_index_creating_preset = partial(
                veg_index_creating,
                contours_objs=contour.id,
                creating_report_obj=IndexCreatingReport,
                veg_index_obj=ActualVegIndex
            )

            # Use a thread pool to process satellite images in parallel
            with ThreadPoolExecutor(max_workers=30) as executor:
                executor.map(veg_index_creating_preset, satellite_images)

    # Record the end time
    end_time = time.time()

    # Calculate the total elapsed time
    elapsed_time = end_time - start_time
    print(f"Processing completed in {elapsed_time:.2f} seconds")
