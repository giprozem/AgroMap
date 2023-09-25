# 📂 *Indexes App*

-----
```
📁 **indexes**
├── 📁 admin
│   ├── 📄 actual_veg_index.py
│   ├── 📄 forms.py
│   ├── 📄 pasture.py
│   └── 📄 satelliteimage.py
├── 📁 index_funcs
│   ├── 📄 common_funcs.py
│   ├── 📄 ndmi_funcs.py
│   ├── 📄 ndre_funcs.py
│   ├── 📄 ndvi_funcs.py
│   ├── 📄 ndwi_funcs.py
│   ├── 📄 savi_funcs.py
│   └── 📄 vari_funcs.py
├── 📁 models
│   ├── 📄 actual_veg_index.py
│   ├── 📄 actual_veg_index_logs.py
│   ├── 📄 pasture.py
│   └── 📄 satelliteimage.py
├── 📁 serializers
│   ├── 📄 actual_veg_index.py
│   └── 📄 statistics_veg_index.py
├── 📁 tests
│   ├── 📄 test_contourstats.py
│   └── 📄 test_indexes.py
├── 📁 views
│   ├── 📄 actual_veg_index.py
│   ├── 📄 download_satellite_images.py
│   ├── 📄 pasture.py
│   └── 📄 statistics_veg_index.py
├── 📄 apps.py
├── 📄 signals.py
├── 📄 translation.py
├── 📄 urls.py
└── 📄 utils.py
```

## 📁 **Admin folder**

-------------
Django's **Admin** is a robust and customizable tool that provides an interface for managing your app's content.

### 📄 [/indexes/admin/actual_veg_index.py](/indexes/admin/actual_veg_index.py)

- `IndexFactAdmin`: **Custom Admin interface for the `ActualVegIndex` model**.
- `IndexMeaningAdmin`: **Custom Admin interface for the `IndexMeaning` model with translation support**.
- `IndexCreatingReportAdmin`: **Custom Admin interface for the `IndexCreatingReport` model**.

### 📄 [/indexes/admin/forms.py](/indexes/admin/forms.py)

This file defines a custom form, `IndexMeaningForm`, for the `IndexMeaning` model. It includes a widget to customize the
appearance of the `description` field in the form.

### 📄 [/indexes/admin/pasture.py](/indexes/admin/pasture.py)

This file registers the `ProductivityClass` and `ContourAverageIndex` models in the Django Admin interface. It uses
mixins for history tracking and translation support.

### 📄 [/indexes/admin/satelliteimage.py.py](/indexes/admin/satelliteimage.py.py)

This file handles the administration of satellite image-related models, including `SciHubAreaInterest`
and `SciHubImageDate`. It includes inline model display, custom widgets for image previews, and additional
functionalities like transforming bounding boxes and displaying thumbnails.

## 📁 **Index_funcs folder**

-------------

### 📄 [/indexes/admin/common_funcs.py](/indexes/admin/common_funcs.py)

- `This function crops a GeoTIFF file based on a given polygon and saves the output to a specified path.`

### 📄 [/indexes/admin/ndmi_funcs.py](/indexes/admin/ndmi_funcs.py)

This script provides functions for handling the Normalized Difference Moisture Index (NDMI) calculations and
visualizations.

- `get_region_of_interest(ndmi, multiplier=1 / 2)`: Calculates the mean value of NDMI for the center of an image.
- `get_ndmi(swir_file, nir_file)`: Computes NDMI for given Short-Wave Infrared (SWIR) and Near Infrared (NIR) images.
- `ndmi_calculator(B08, B11, saving_file_name)`: Visualizes and calculates NDMI for SWIR and NIR bands, returning an
  image.
- `average_ndmi(swir_file, nir_file)`: Calculates the average NDMI for given SWIR and NIR images.

### 📄 [/indexes/admin/ndre_funcs.py](/indexes/admin/ndre_funcs.py)

This script provides functions for handling the Normalized Difference Red Edge (NDRE) calculations and visualizations.

- `get_region_of_interest(ndre, multiplier=1 / 2)`: Calculates the mean value of NDRE for the center of an image.
- `get_ndre(red_file, nir_file)`: Computes NDRE for given Red and Near Infrared (NIR) images.
- `ndre_calculator(B07, B8A, saving_file_name)`: Visualizes and calculates NDRE for Red and NIR bands, returning an
  image.
- `average_ndre(red_file, nir_file)`: Calculates the average NDRE for given Red and NIR images.

These scripts are used for calculating vegetation-related indices (NDMI and NDRE) and generating visualizations based on
satellite imagery.

### 📄 [/indexes/admin/ndvi_funcs.py](/indexes/admin/ndvi_funcs.py)

This module contains functions for working with the Normalized Difference Vegetation Index (NDVI) and includes:

- `get_region_of_interest`: Calculates the mean NDVI value for the center of an image.
- `get_ndvi`: Calculates NDVI for given Red and Near Infrared (NIR) images.
- `ndvi_calculator`: Visualizes and calculates NDVI for Red and NIR bands, returning an image.
- `average_ndvi`: Calculates the average NDVI for given Red and NIR images.

### 📄 [/indexes/admin/ndwi_funcs.py](/indexes/admin/ndwi_funcs.py)

This module contains functions for working with the Normalized Difference Water Index (NDWI) and includes:

- `get_region_of_interest`: Calculates the mean NDWI value for the center of an image.
- `get_ndwi`: Calculates NDWI using Green and Near Infrared (NIR) bands.
- `ndwi_calculator`: Visualizes and calculates NDWI for Green and NIR bands, returning an image.
- `average_ndwi`: Calculates the average NDWI for given Green and NIR images.

### 📄 [/indexes/admin/savi_funcs.py](/indexes/admin/savi_funcs.py)

This module contains functions for working with the Soil Adjusted Vegetation Index (SAVI) and includes:

- `get_region_of_interest`: Calculates the mean SAVI value for the center of an image.
- `get_savi`: Calculates SAVI using Red and Near Infrared (NIR) bands with a given soil brightness correction factor, L.
- `savi_calculator`: Visualizes and calculates SAVI for Red and NIR bands, returning an image.
- `average_savi`: Calculates the average SAVI for given Red and NIR images.

### 📄 [/indexes/admin/vari_funcs.py](/indexes/admin/vari_funcs.py)

This module contains functions for working with the Visible Atmospherically Resistant Index (VARI) and includes:

- `get_region_of_interest`: Calculates the mean VARI value for the center of an image.
- `get_vari`: Calculates VARI using Red, Green, and Blue bands.
- `vari_calculator`: Visualizes and calculates VARI for Red, Green, and Blue bands, returning an image.
- `average_vari`: Calculates the average VARI for given Red, Green, and Blue images.

These functions are used for processing and analyzing remote sensing data related to vegetation, water, and soil
conditions. They provide tools for calculating and visualizing various vegetation and environmental indices.

## 📁 **Models folder**

-------------

Models 📋 in Django define the structure of a database table.

### 📄 [/indexes/models/actual_veg_index.py](/indexes/models/actual_veg_index.py)

This file defines Django models related to actual vegetation index data, index meanings, and AI-based predicted
vegetation index values.

#### `ActualVegIndex` Model

The `ActualVegIndex` model stores information about actual vegetation index data and includes:

- `index_image`: Field to upload the index image.
- `average_value`: Field for the average index value.
- `meaning_of_average_value`: Field to link to the meaning of the average index value.
- `index`: Field to link to the vegetation index.
- `contour`: Field to link to the field contours.
- `date`: Field to specify the analysis date.
- `history`: Field to track historical records of changes.

#### `IndexMeaning` Model

The `IndexMeaning` model defines the meaning and allowable range of values for vegetation indexes. It includes:

- `index`: Field to link to the associated vegetation index.
- `min_index_value`: Field for the minimum index value.
- `max_index_value`: Field for the maximum index value.
- `description`: Field to provide a description of the index's significance.

#### `PredictedContourVegIndex` Model

The `PredictedContourVegIndex` model stores predicted vegetation index values associated with specific contours and
includes:

- `index_image`: Field to upload the index image.
- `average_value`: Field for the average index value.
- `meaning_of_average_value`: Field to link to the meaning of the index value.
- `index`: Field to link to the vegetation index.
- `contour`: Field to link to the contour AI.
- `date`: Field to specify the analysis date.
- `history`: Field to track historical records of changes.

### 📄 [/indexes/models/actual_veg_index_logs.py](/indexes/models/actual_veg_index_logs.py)

This file defines models related to reports about the creation and processing of data related to vegetation indexes and
satellite images.

#### `IndexCreatingReport` Model

The `IndexCreatingReport` model stores reports about the creation and processing of data related to vegetation indexes
and satellite images. It includes fields for contour, vegetation index, satellite image, processing status, and
processing errors.

#### `ContourAIIndexCreatingReport` Model

The `ContourAIIndexCreatingReport` model stores reports about the creation and processing of data related to vegetation
indexes and satellite images, particularly in the context of AI-based contour analysis. It includes fields for contour
AI, vegetation index, satellite image, processing status, and processing errors.

These models provide a structured way to store and manage data related to vegetation indexes, their meanings, and
reports on data creation and processing.

### 📄 [/indexes/models/pasture.py](/indexes/models/pasture.py)

This file defines Django models related to productivity classes, contour average index values, satellite image sources,
bands, layers, areas of interest, and Sentinel-2 satellite images.

#### `ProductivityClass` Model

The `ProductivityClass` model represents categories or classes related to productivity. It includes fields for the name
and an optional description for each productivity class.

#### `ContourAverageIndex` Model

The `ContourAverageIndex` model calculates and stores the average index values for specific contours. It provides fields
to link to a contour, store the calculated average value, associate a productivity class, specify the start and end date
of the calculation period, and keep a historical record of changes.

#### `SatelliteImageSource` Model

The `SatelliteImageSource` model stores information about various sources of satellite images. It allows you to define
and manage different sources by providing a name and a description for each source.

#### `SatelliteImageBand` Model

The `SatelliteImageBand` model stores information about various bands present in satellite images. It allows you to
define and manage different bands by providing a name and a description for each band.

#### `SatelliteImageLayer` Model

The `SatelliteImageLayer` model manages and associates satellite image layers with their sources and bands. It provides
fields to link to image files, specify the source of the image, and indicate the band to which the image belongs.

#### `SciHubAreaInterest` Model

The `SciHubAreaInterest` model stores geographic polygons representing areas of interest on the Earth's surface for the
acquisition of satellite images. It provides a field to store these polygons.

#### `SciHubImageDate` Model

The `SciHubImageDate` model stores information about Sentinel-2 satellite images, including their metadata and file
attachments. It provides fields to store image-related data, such as image date, associated area of interest, image
files for different bands, and other relevant details.

These models collectively provide a structured way to manage data related to productivity classes, contour average index
values, satellite image sources, bands, layers, areas of interest, and Sentinel-2 satellite images within the Django
application.

### 📄 [/indexes/models/satelliteimage.py](/indexes/models/satelliteimage.py)

This file defines Django models related to satellite images, including their sources, bands, layers, areas of interest,
and Sentinel-2 satellite images.

#### `SatelliteImageSource` Model

The `SatelliteImageSource` model stores information about various sources of satellite images. It allows you to define
and manage different sources by providing a name and a description for each source.

#### `SatelliteImageBand` Model

The `SatelliteImageBand` model stores information about various bands present in satellite images. It allows you to
define and manage different bands by providing a name and a description for each band.

#### `SatelliteImageLayer` Model

The `SatelliteImageLayer` model is designed to manage and associate satellite image layers with their sources and bands.
It provides fields to link to image files, specify the source of the image, and indicate the band to which the image
belongs.

#### `SciHubAreaInterest` Model

The `SciHubAreaInterest` model is designed to store geographic polygons representing areas of interest on the Earth's
surface for the acquisition of satellite images. It provides a field to store these polygons.

#### `SciHubImageDate` Model

The `SciHubImageDate` model is designed to store information about Sentinel-2 satellite images, including their metadata
and file attachments. It provides fields to store image-related data, such as image date, associated area of interest,
image files for different bands, and other relevant details.

These models collectively provide a structured way to manage data related to satellite images and their associated
attributes within the Django application.

## 📁 **Serializers folder**

-------------

### 📄 [/indexes/serializers/actual_veg_index.py](/indexes/serializers/actual_veg_index.py)

This file contains serializers for models related to actual vegetation index data,
including `ActualVegIndex`, `IndexMeaning`, and `PredictedContourVegIndex`. It defines serializers for these models,
allowing data to be serialized for use in the Django REST framework.

- `IndexMeaningSerializer`: Serializes the `IndexMeaning` model, excluding certain fields.
- `ActualVegIndexSerializer`: Serializes the `ActualVegIndex` model, including all fields and nested fields for
  associated models.
- `SatelliteImageSerializer`: A serializer for the `SatelliteImage`, which is essentially the same as
  the `ActualVegIndex` serializer and encompasses all fields.
- `PredictedContourActuaVegIndexSerializer`: Serializes the `PredictedContourVegIndex` model, including all fields and
  nested fields for associated models.

### 📄 [/indexes/serializers/statistics_veg_index.py](/indexes/serializers/statistics_veg_index.py)

This file defines serializers for generating statistics related to vegetation index data, including a compact serializer
for `ActualVegIndex` and a custom representation of the `Contour` model that incorporates data from
associated `VegIndex` models.

- `VegIndexSerializer`: A compact serializer for the `ActualVegIndex` model, extracting the index name, average value,
  and date.
- `ContourStatisticsSerializer`: A custom representation of the `Contour` instance that enhances basic serialized data
  with additional vegetation index information.

## 📁 **[Test folder](/indexes/tests)**

-------------


The "tests" folder is used for writing automated test cases to verify the correctness of your Django application's
functionality. It includes test cases, fixtures, and configurations.

Purpose:
The "tests" folder is meant for creating automated tests for your Django application.
It helps in verifying that your application's functionality works as intended, especially after making code changes or
adding new features.
Tests provide a safety net to catch and fix bugs early in the development process.
Django provides a built-in testing framework that makes it easier to write and run tests.
Contents:
Test cases: Python files containing classes that inherit from Django's TestCase class. These classes define methods for
testing specific parts of your application.
Test fixtures: Data files or functions that set up the initial state of your database for testing purposes.
Test runner configuration: A configuration file (e.g., settings.py) that specifies testing settings, such as the
database to use during testing.
Helper functions: Utility functions that assist in writing test cases.

## 📁 **[Views folder](/indexes/views)**

-------------

The "views" folder in a Django project contains Python files that define the logic for handling HTTP requests and
rendering HTML templates. Views are an integral part of the Django web framework, and they determine how data is
presented to users in web applications.

Purpose:
Views are responsible for processing incoming HTTP requests and returning appropriate responses.
They encapsulate the business logic of your application and handle interactions with the database.
Views can render HTML templates, return JSON data, or perform other actions based on the request.
Django follows the Model-View-Controller (MVC) architectural pattern, where views correspond to the "controller"
component.
Contents:
View functions: Python functions that define how to handle specific URL patterns and HTTP methods. These functions may
use models, query databases, and render templates.
Class-based views: Python classes that provide a more organized way to handle complex views and reuse code.
Template files: HTML templates that define the structure and layout of web pages rendered by views.
URL routing configuration: A file (usually urls.py) where you specify the URL patterns and associate them with view
functions or classes.
