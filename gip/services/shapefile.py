import os
import zipfile
import shutil
import tempfile
from typing import Any

from osgeo import ogr

import geopandas as gpd

import rarfile


from django.contrib.gis.geos import GEOSGeometry
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework.exceptions import NotAcceptable


class UploadAndExtractService:
    """Utility for uploading and processing data from a zip archive containing shapefiles."""

    TEMP_FOLDER = "/tmp/shapefile_temp"

    def __init__(self, zip_file, model):
        self.zip_file = zip_file
        self.model = model

    def _create_temp_folder(self) -> None:
        """Create a temporary folder for file operations."""
        os.makedirs(self.TEMP_FOLDER, exist_ok=True)

    def _save_zip(self) -> str:
        """Save the zip file to the temporary folder."""
        temp_path = os.path.join(self.TEMP_FOLDER, self.zip_file.name)
        with open(temp_path, "wb+") as destination:
            for chunk in self.zip_file.chunks():
                destination.write(chunk)
        return temp_path

    def _unzip_file(self, archive_path: str) -> str:
        """Unzip the file into the temporary folder."""
        archive_extract_path = os.path.join(self.TEMP_FOLDER, "extracted")
        os.makedirs(archive_extract_path, exist_ok=True)

        if archive_path.lower().endswith(".zip"):
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                zip_ref.extractall(archive_extract_path)
        elif archive_path.lower().endswith(".rar"):
            with rarfile.RarFile(archive_path, "r") as rar_ref:
                rar_ref.extractall(archive_extract_path)

        return archive_extract_path

    def _process_shapefile(self, shapefile_path: str) -> None:
        """Process a shapefile."""
        driver = ogr.GetDriverByName("ESRI Shapefile")
        dataset = driver.Open(shapefile_path)
        layer = dataset.GetLayer()
        for feature in layer:
            geometry = GEOSGeometry(feature.GetGeometryRef().ExportToWkt())
            attributes = {
                feature.GetFieldDefnRef(field_index).GetName(): feature.GetField(
                    field_index
                )
                for field_index in range(feature.GetFieldCount())
            }
            code_soato = None
            code_soato = attributes.get("code_soato")
            if code_soato is None:
                code_soato = attributes.get("code_soa")

            canton_id = attributes.get("conton")

            if canton_id is None:
                raise NotAcceptable(detail="property canton id is required", code=400)

            type_id = attributes.get("type")
            year = attributes.get("year")
            productivity = attributes.get("producti")
            predicted_productivity = attributes.get("predicte")
            culture = attributes.get("culture")
            ink = attributes.get("ink")
            eni = attributes.get("eni")
            farmer = attributes.get("farmer")
            pasture_list: list = attributes.get("pasture") or []
            if pasture_list is not None:
                pasture_culture = [i for i in pasture_list]

            contour = self.model(
                polygon=geometry,
                code_soato=code_soato,
                conton_id=canton_id,
                type_id=type_id,
                year=year,
                ink=ink,
                culture_id=culture,
                productivity=productivity,
                predicted_productivity=predicted_productivity,
                farmer=farmer,
                eni=eni,
            )
            contour.save()
            contour.pasture_culture.add(*pasture_culture)

    def _cleanup(self, temp_path: str, extract_path: str) -> None:
        """Clean up temporary files and folders."""
        os.remove(temp_path)
        shutil.rmtree(extract_path)

    def execute(self) -> None:
        """Main method to execute upload and processing."""
        self._create_temp_folder()
        temp_path = self._save_zip()
        try:
            extract_path = self._unzip_file(temp_path)
            path = os.path.join(extract_path)
            shapefile_found = False

            # Check if there is a 'layers' directory
            layers_path = os.path.join(path, "layers")
            if os.path.isdir(layers_path):
                for file_name in os.listdir(layers_path):
                    file_path = os.path.join(layers_path, file_name)
                    if os.path.isfile(file_path):
                        if file_path.lower().endswith((".shp", ".shx", ".dbf", ".prj")):
                            shapefile_found = True
                            with transaction.atomic():
                                self._process_shapefile(file_path)
                                self._cleanup(temp_path, extract_path)
                                break

            else:
                for file_name in os.listdir(path):
                    file_path = os.path.join(path, file_name)
                    if os.path.isfile(file_path):
                        if file_path.lower().endswith((".shp", ".shx", ".dbf", ".prj")):
                            shapefile_found = True
                            with transaction.atomic():
                                self._process_shapefile(file_path)
                                self._cleanup(temp_path, extract_path)
                                break

            if not shapefile_found:
                self._cleanup(temp_path, extract_path)
                raise Exception("No shapefile found in the archive.")

        except Exception as e:
            self._cleanup(temp_path, extract_path)
            raise NotAcceptable(e)


class ExportAndZipService:

    """Utility for exporting data as shapefile and geojson, and packaging them into a zip archive."""

    def __init__(self, model) -> None:
        self.model = model

    def get_qeuryset(self, pk: int) -> Any:
        """Retrieve the queryset based on the provided key."""

        work_model = get_object_or_404(self.model, pk=pk)
        return work_model

    def create_geojson(self, qs: Any) -> str:
        """Create a geojson representation of the data."""

        geojson = serialize("geojson", [qs])
        return geojson

    def create_zip_file(self, geojson: str) -> bytes:
        """Create a zip archive containing data in shapefile and geojson formats."""
        with tempfile.TemporaryDirectory() as temp_dir:
            layer_dir = os.path.join(temp_dir, "layers")
            os.makedirs(layer_dir)

            gdf = gpd.read_file(geojson)
            gdf["created_at"] = gdf["created_at"].astype(str)
            gdf["updated_at"] = gdf["updated_at"].astype(str)

            shp_path = os.path.join(layer_dir, "data.shp")
            gdf.to_file(shp_path)

            shutil.make_archive(os.path.splitext(temp_dir)[0], "zip", temp_dir)

            zip_file_path = os.path.splitext(temp_dir)[0] + ".zip"
            with open(zip_file_path, "rb") as zip_file:
                return zip_file.read()

    def execute(self, pk: int) -> bytes:
        """Main method to execute export and packaging."""
        qs = self.get_qeuryset(pk=pk)
        geojson = self.create_geojson(qs=qs)
        return self.create_zip_file(geojson=geojson)
