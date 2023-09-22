# Administrative Panel.

Documentation for using the "AgroMap" administrative panel.

## What You'll Need

+ [Windows/Linux/Mac] Basic computer usage skills
+ [Internet] Internet access
+ [GIS] Understanding of geographic coordinates (longitude/latitude)
+ [Kyrgyzstan] Knowledge of the geographical boundaries of regions, districts, and counties.


## Authorization

To use the administrative panel, you need to log in.

![alt-текст](images/login.png)

Enter the administrator's login and password. After that, you will be redirected to the main page.

## Main Page
![alt-текст](images/main-page.png)

You can also change the language or log out by clicking on the corresponding tabs in the top right corner.

![alt-текст](images/lang-page.png)

On the left side of the panel, there is navigation for objects and categories.

![alt-текст](images/verbose.png)

## Creating Contours

To create a contour, you need to create objects such as "Region," "District," "County," and "Soil Type."

Note: It is necessary to follow the hierarchy of objects. For example, to create a county, you need to specify the district, and for a district, specify the region.

### Creating a Contour

Select the "Field Contours" object on the left and click "Add Field Contours." You will be taken to the contour creation page.

![alt-текст](images/contour-form.png)

Fill in the necessary data; mandatory fields will be marked with a red asterisk *. The vegetation type will be automatically determined if data about the type is available in the database.

#### Field Definitions

+ [SOATO Code] - The system for designating objects of administrative-territorial division of the Kyrgyz Republic.

+ [Productivity] - Productivity is measured in centners per hectare (c/ha), and values above 1.6 are considered good.

+ [Vegetation Type] - A list of plant species that grow in the fields within this contour.

+ [Predicted Productivity] - Productivity is determined by artificial intelligence (AI) trained on initial data. 

+ [Is deleted] - The status of the object in the database indicates non-operation and is marked with a checkbox.

+ [INC] - Identification number of the contour assigned to uniquely identify and track it in the database.

+ [ЕНИ] - ?
+ [Юридически подтвержденный] - Юридически подтвержденный статус объекта в базе данных также обозначается галочкой.

+ [Contour] - Important*: The contour should not extend beyond the borders of Kyrgyzstan.

#### Creating Field Types

To create a new field type, go to the object list and click "Add..." Fill in the necessary fields in the form.

#### Creating Soil Types

Usually, there is no need to create a new soil type. However, if required, follow the steps from the previous sections. Click "Add..." and fill in the necessary data in the form.

#### Creating Soil Type Contours

This object is related to soil types and is used to indicate contours of different soil types on the map.

![alt-текст](images/land-contour.png)

#### Creating Crops

To create a new crop type, go to the object list and click "Add...". Fill in the necessary fields in the form.

#### Creating Productivity

To create a new productivity type, go to the object list and click "Add...". Fill in the necessary fields in the form.

Productivity is directly related to crop objects.