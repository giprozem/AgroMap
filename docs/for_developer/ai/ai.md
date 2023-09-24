
## 📁 **Admin folder**

```
ai
├── 📁 admin/
    ├──📄 create_dataset.py
    ├──📄 predicted_contour.py
    ├──📄 productivity.py

├── 📁 culture_Ai/
    ├──📄 predicted_contour.py

├── 📁 migrations/
├── 📁 models/
    ├──📄 create_dataset.py
    ├──📄 predicted_contour.py
    ├──📄 productivity.py
├── 📁productivity_funcs
    ├──📄 predicting.py

├── 📁 serializers/
    ├──📄 create_dataset.py
    ├──📄 predicted_contour.py
    ├──📄 productivity.py

├── 📁 tests/
    ├──📄 factories.py
    ├──📄 tests.py

├── 📁 utils/
    ├──📄 create_dataset.py
    ├──📄 predicted_contour.py

├── 📁 views/
    ├──📄 create_dataset.py
    ├──📄 heat_map_ndvi.py
    ├──📄 predict_culture.py
    ├──📄 predicted_contour.py
    ├──📄 productivity.py

├── 📄 apps.py
├── 📄 authentication.py
├── 📄 translation.py
├── 📄 urls.py
```

Django's **Admin** 🛠 is a robust and customizable tool that provides an interface for managing your app's content. The "Account" application uses the "admin" folder to oversee user data.

### 📄 [/ai/admin/create_dataset.py](/ai/admin/create_dataset.py)

- `DatasetAdmin`: **Admin settings for the Dataset model** with read-only fields 'created_at' and 'updated_at'.
- `ProcessAdmin`: **Admin settings for the Process model**.
- `Merge_BandsAdmin`: **Admin settings for the Merge_Bands model**.
- `Create_RGBAdmin`: **Admin settings for the Create_RGB model**.
- `Cut_RGB_TIFAdmin`: **Admin settings for the Cut_RGB_TIF model**.
- `AI_FoundAdmin`: **Admin settings for the AI_Found model**.
- `CreateDescriptionAdmin`: **Admin settings for the CreateDescription model**.

### 📄 [/ai/admin/predicted_contour.py](/ai/admin/predicted_contour.py)

- `VegIndexTabularInline`: **Tabular inline for the PredictedContourVegIndex model**. Displays NDVI visualizations and readonly fields to prevent edits.
- `Contour_AIAdmin`: **Leaflet-enabled admin for the Contour_AI model**. Supports inline vegetation indices and offers filtering and search functionalities.
- `Images_AIAdmin`: **Admin settings for the Images_AI model** with an HTML-rendered photo view.
- `YoloAdmin`: **Admin settings for the Yolo model**. No specific customizations or restrictions defined for this admin.

### 📄 [/ai/admin/productivity.py](/ai/admin/productivity.py)

- `ProductivityMLAdmin`: **Admin settings for the ProductivityML model**. No specific customizations or restrictions defined for this admin.
- `PredictedContourVegIndexAdmin`: **Admin settings for the PredictedContourVegIndex model**. Displays NDVI visualizations, index values, and other attributes with specific readonly fields. Allows filtering, custom list views, and pagination.
- `ContourAIIndexCreatingReportAdmin`: **Admin settings for the ContourAIIndexCreatingReport model**. No specific customizations or restrictions defined for this admin.

## 📁 **Migration folder**

Migrations 🔄 in Django keep track of model changes and help in smoothly transitioning database schemas.

## 📁 **Models folder**

Models 📋 in Django define the structure of a database table.

### 📄 [/ai/models/create_dataset.py](/ai/models/create_dataset.py)

- `Dataset`: **Model to store and manage information related to datasets**. Supports file uploads for datasets.
- `Process`: **Singleton model representing a single process or task**. Contains attributes like the running state and process number.
- `Merge_Bands`: **Singleton model representing the process of merging image bands**. Contains attributes like completion state and process number.
- `Create_RGB`: **Singleton model representing the creation of color images process**. Contains attributes like completion state and process number.
- `Cut_RGB_TIF`: **Singleton model representing the process of cropping color images in TIFF format**. Contains attributes like completion state and process number.
- `AI_Found`: **Singleton model representing a contour search process, potentially using AI**. Contains a completion state attribute.
- `CreateDescription`: **Singleton model storing instructions for creating a dataset**. Contains a textual description field.

### 📄 [/ai/models/predicted_contour.py](/ai/models/predicted_contour.py)

- `Images_AI`: **Model to store image files used for AI-related processes**. Supports image uploads.
- `Contour_AI`: **Model to store AI-detected contours of land features**. Includes attributes like region, land type, contour geometry, year, productivity, area in hectares, and associated image.
- `Yolo`: **Singleton model designed to store a YOLO contour detection model**. Contains the model file for contour detection.

### 📄 [/ai/models/productivity.py](/ai/models/productivity.py)

- `ProductivityML`: 📈 **Model to store a machine learning model file used for productivity prediction**. Supports model file uploads for productivity prediction.

## 📁 **Culture AI**

This module's Satellite Predictor/Culture AI 🛠 is a specialized tool crafted for the purpose of analyzing satellite images. Utilizing the power of neural networks, it facilitates the extraction of meaningful information from the distinct bands of these images and classifies them.

### 📄 [/ai/culture_AI/predict_culture.py](/ai/culture_AI/predict_culture.py)

- `FeedForwardNN`: **PyTorch neural network model** for regression or classification tasks. It contains input, hidden, and output layers with ReLU activation.

- `extract_features_from_bands`: **Function to extract statistical features** (mean values) from raster bands. It takes red, near-infrared, and shortwave infrared bands as input.

- `predict_from_features`: **Function to make predictions** using the extracted features. It takes features, a PyTorch model, and a scaler for normalization as input.

- `predict_from_raster_bands`: **Function to predict a class** based on raster bands. It reads raster bands from file paths, extracts features, and makes predictions using a PyTorch model and scaler.

- Other Imports: Import statements for required libraries like NumPy, Rasterio, PyTorch, GDAL, and Pickle.

- Initialization: Initializing the model, loss function, and optimizer, setting the device (CPU in this case).

- `FeedForwardNN` Class: A class representing a feedforward neural network with input, hidden, and output layers.

- Model Loading: Loading a pre-trained PyTorch model and a scaler from saved files.

- Model Evaluation: Evaluating the model by passing input features through it and making predictions.

- Predicted Class: Getting the predicted class based on the model's output.

- Input Data: Reading raster bands from file paths and performing feature extraction.

- `pickle` Usage: Loading a saved scaler and saving/loading the PyTorch model.

- Function Descriptions: Providing comments explaining the purpose of each function and section of the code.

## 📁 **Culture AI**

Productivity Predictor 🛠 is a tool designed to predict productivity levels based on input features. It uses a pre-trained linear regression model to make predictions.

### 📄 [/ai/productivity_funcs/predicting.py](/ai/productivity_funcs/predicting.py)

- `productivity_model_path`: A file path pointing to the location of the trained productivity prediction model (in .pkl format).

- `productivity_predict`: **Function to predict productivity** based on input features using a trained linear regression model.

  - Parameters:
    - `predicting`: The input feature(s) for which productivity is to be predicted.
    - `model_path`: (Optional) The file path of the trained model. Default is set to `productivity_model_path`.

  - Process:
    - It loads the trained linear regression model from the specified `.pkl` file using `pickle`.
    - The input features are structured as a list of lists to match the expected format.
    - The model makes predictions on the input features using the `predict` method.
    - The predicted productivity value is returned as a floating-point number.

- Other Imports: Import statement for the `pickle` library, required for loading the trained model from the file.

## 📁 **Serializers folder**

Serializers 🔄 in Django convert data for web APIs.

### - 📄 [/ai/serializers/create_dataset.py](/ai/serializers/create_dataset.py)

- `CreateDescriptionSerializer`: **Serializer for the CreateDescription model**.

  - Description: This serializer is used to convert instances of the `CreateDescription` model into JSON format for use in Django REST framework. It specifies the model it is serializing and excludes the `description` field from serialization.

  - `Meta` Class:
    - `model`: Specifies the model that this serializer is associated with (`CreateDescription` in this case).
    - `exclude`: Specifies which fields to exclude from serialization. In this case, it excludes the `description` field, which is not included in the serialized output.

### - 📄 [/ai/serializers/predicted_contour.py](/ai/serializers/predicted_contour.py)

- `Contour_AISerializer`: **Serializer for the Contour_AI model**. Serializes all fields from the Contour_AI model and includes nested serializers for related fields (soil_class, type, culture). Additionally, it customizes the representation method to include region and district information if available.

- Custom Methods:
  - `to_representation`: A custom representation method to add region and district data to the serialized output. It includes region and district information if they exist for the contour.

- `UpdateContour_AISerializer`: **Serializer for updating the Contour_AI model**. Serializes all fields from the Contour_AI model and includes custom methods for validation and polygon checks.

- Custom Methods:
  - `to_representation`: A custom representation method to add `region_id` and `district_id` fields to the serialized output based on the `conton` relationship.
  - `is_polygon_inside_Kyrgyzstan`: Method to check if a given polygon is inside the boundaries of Kyrgyzstan using geospatial queries.
  - `get_district`: Method to get the district ID based on the polygon using geospatial queries.
  - `get_db_district`: Method to get the district ID from the database based on the `conton` relationship.
  - `validate_district`: Method to validate if the district based on the polygon matches the district in the database. Raises an exception if they do not match.
  - `is_valid_year`: Method to validate the year attribute. Checks if the year is within a valid range.
  - `validate`: Custom validation method for the serializer. Checks if the polygon is inside Kyrgyzstan, validates the district, and ensures the year is within a valid range.

- Other Imports: Import statements for required libraries, models, serializers, and exceptions used in the code.

### - 📄 [/ai/serializers/predicted_contour.py](/ai/serializers/predicted_contour.py)

- `ContourAISerializer`: **Serializer for the Contour_AI model**. Serializes all fields from the Contour_AI model.

- `ContourAIStatisticsSerializer`: **Serializer for the Contour_AI model with additional statistics**. Excludes the 'polygon' field from serialization and includes custom representation to add statistics for veg index data.

  - Custom Methods:
    - `to_representation`: A custom representation method to include additional statistics for veg index data. It uses the `VegIndexSerializer` to serialize related veg index data and adds them to the serialized output as additional fields.

- Other Imports: Import statements for required models and serializers used in the code.

## 📁 **Tests folder**

The "tests" folder 🧪 ensures the app's code reliability.

- 📄 Files:
  - [factories.py](/ai/tests/factories.py)
  - [tests.py](/ai/tests/tests.py)

---

## 📁 **Views folder**

Views 👀 in Django control how data is displayed and processed.

### - 📄 [/ai/views/create_dataset.py](/ai/views/create_dataset.py)

- `CreateAPIView`: **API view for creating datasets**. This view is accessible only to admin users and provides the ability to start a dataset creation process.

  - Permissions: Only admin users (`IsAdminUser`) are allowed to access this view.

  - Methods:
    - `get`: Handles GET requests to check the dataset creation process status and initiate a new process if it's not running. Also, it sends notifications when a new dataset is created.

- `CreateDescriptionAPIView`: **API view for getting dataset creation instructions**. This view is accessible only to admin users and provides instructions for creating a dataset.

  - Permissions: Only admin users (`IsAdminUser`) are allowed to access this view.

  - Methods:
    - `get`: Handles GET requests to retrieve instructions for creating a dataset. It uses the `CreateDescription` model and serializer to provide detailed instructions.

- Signals and Receivers: The code includes a signal and receiver combination that triggers a notification when a new dataset is created (`post_save` signal for the `Dataset` model).

- Swagger Documentation: The `CreateDescriptionAPIView` includes Swagger documentation using the `swagger_auto_schema` decorator to describe the API operation.

- Other Imports: Import statements for required modules, models, and serializers used in the code.

## 📄 **apps.py**

### - 📄 [/ai/apps.py](/ai/apps.py)

It's where the app's configurations 🛠️ are stored.

## 📁 **Utils**

Utils 🛠 is a function designed to create a dataset suitable for training machine learning models, particularly for object detection tasks in images. Here's a brief description for documentation:

### - 📄 [/ai/utils/create_dataset.py](/ai/utils/create_dataset.py)

- `create_dataset()`: 📂 **Dataset Creation Function**

  This function is designed to create a dataset for training machine learning models, specifically for object detection tasks in images.

  - Functionality:
    - Iterates through the cutted TIFF files in the 'media/cutted_tiff' directory.
    - Opens each raster file using rasterio and extracts its bounding box in the original CRS.
    - Transforms the bounding box to EPSG:4326 (WGS84) CRS and creates a Shapely Polygon.
    - Retrieves GeoJSON polygons from the database that are properly contained within the bounding box.
    - Converts the GeoJSON data to a list.
    - Saves the raster image as a PNG in the 'media/dataset/train/images/' directory.
    - Converts the coordinates of contour polygons to image-relative coordinates and generates label text.
    - Saves the label text in a corresponding '.txt' file in the 'media/dataset/train/labels/' directory.
    - Creates a ZIP archive of the dataset directory.
    - Saves the ZIP archive as a Dataset object with today's date as the name.
    - Removes the temporary ZIP archive file.

  - Note:
    - This function is intended for creating a dataset for object detection tasks and includes the conversion of coordinate systems, image saving, and label generation.

  - Usage:
    - Call this function to generate the dataset.

- Other Imports: Import statements for required modules and libraries used in the function.

### - 📄 [/ai/utils/predicted_contour.py](/ai/utils/predicted_contour.py)

- `predicted_contour()`: **Contour Prediction Function**

  This function detects object outlines in images using the YOLO (You Only Look Once) model. It performs the following steps:

  - Fetches the YOLO model from the database.
  - Iterates through image files in the 'media/TCI/' directory.
  - Predicts object outlines using the YOLO model.
  - Extracts mask coordinates and confidences from the results.
  - Converts pixel coordinates to physical coordinates.
  - Generates simplified polygons from mask coordinates.
  - Computes the intersection area with existing contours in the database.
  - Creates new Contour_AI objects for detected contours with an intersection area of less than 30%.

- `clean_contour_and_create_district()`: **Contour Cleaning and District Creation Function**

  This function cleans and assigns districts to contours based on their geographical locations. It performs the following steps:

  - Retrieves Contour_AI objects.
  - Identifies the intersecting district for each contour and updates the district_id field.
  - Calculates the area in hectares for contours and updates the area_ha field.
  - Deletes contours with an area less than 1.0 ha or greater than 70.0 ha.

- Other Imports: Import statements for required modules, libraries, and models used in the functions.

These functions collectively handle the prediction of contours in images and the processing of geographical data for contours and districts.

---

## 📄 **translation.py**

[Translate models 🌐.](/account/translation.py)

---

## 📄 **urls.py**

[It's where the url's configurations 🛠️ are stored.](/account/urls.py)
