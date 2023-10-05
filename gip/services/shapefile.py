from typing import Any
from pathlib import Path

import json
import os
import zipfile
import shutil
import tempfile
import rarfile

from osgeo import ogr
import geopandas as gpd

from rest_framework.exceptions import NotAcceptable

from django.contrib.gis.geos import GEOSGeometry
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from django.db import transaction

from gip.exceptions.shapefile_exceptions import (
    ServerAlertException,
    ShapeFileNotFoundException,
)


class UploadAndExtractService:
    """Utility for uploading and processing data from a zip archive containing shapefiles."""

    TEMP_FOLDER = "/tmp/shapefile_temp"
    SHAPEFILE_FORMAT = (".shp", ".shx", ".dbf", ".prj")

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

            canton_id = attributes.get("conton") or None

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
                conton_id=canton_id if canton_id else None,
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
            for root, dirs, files in os.walk(path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if file_path.lower().endswith(self.SHAPEFILE_FORMAT):
                        with transaction.atomic():
                            self._process_shapefile(file_path)
                            self._cleanup(temp_path, extract_path)
                            break

                    if not shapefile_found:
                        self._cleanup(temp_path, extract_path)
                        raise ShapeFileNotFoundException()

        except Exception as e:
            raise ServerAlertException(detail=e, code=500, exception_message=e)


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
        """Convert str to dict"""
        geojson_to_dict = json.loads(geojson)
        """Get properties and update then"""
        geojson_props = geojson_to_dict.get("features")[0].get("properties")
        geojson_props.update({"conton_name": qs.conton.name, "type_name": qs.type.name})
        """Convert dict to str"""
        geojson_dict_to_str = json.dumps(geojson_to_dict)
        return geojson_dict_to_str

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
        try:
            qs = self.get_qeuryset(pk=pk)
            geojson = self.create_geojson(qs=qs)
            return self.create_zip_file(geojson=geojson)

        except:
            pass  # TODO update exception
