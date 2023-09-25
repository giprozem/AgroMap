# 📂 **Culture Model App**

-----
```
📁 **culture_model**
│
├── 📁 admin
│   ├── 📄 common.py
│   └── 📄 pasture_culture.py
│
├── 📁 migrations
│
├── 📁 models
│   ├── 📄 decade.py
│   ├── 📄 index_plan.py
│   ├── 📄 pasture_culture.py
│   ├── 📄 phase.py
│   └── 📄 vegetation_index.py
│
├── 📁 serializers
│   └── 📄 index.py
│
├── 📁 tests
│   ├── 📄 factories.py
│   └── 📄 tests.py
│
├── 📁 views
│   └── 📄 veg_indexes.py
│
├── 📄 apps.py
├── 📄 authentication.py
├── 📄 translation.py
└── 📄 urls.py
```

## 📁 **Admin folder**

Django's **Admin** 🛠 is a robust and customizable tool that provides an interface for managing your app's content. The "Culture model" application uses the "admin" folder to oversee user data

- 📄 [/culture_model/admin/common.py](/culture_model/admin/common.py)

**Admin Configurations for Django Models**

- **Decade Model Admin (DecadeAdmin)**:
  - **Purpose**: The `DecadeAdmin` class is used to customize the Django admin interface for the `Decade` model. It provides a simple history admin for tracking changes to `Decade` instances.
  - **Registration**: The `Decade` model is registered with the admin site using `@admin.register(Decade)` decorator.
  
- **VegetationIndex Model Admin (IndexAdmin)**:
  - **Purpose**: The `IndexAdmin` class is used to customize the Django admin interface for the `VegetationIndex` model. It provides a simple history admin for tracking changes to `VegetationIndex` instances and integrates with model translation.
  - **Registration**: The `VegetationIndex` model is registered with the admin site using `@admin.register(VegetationIndex)` decorator.
  - **Customization**: The `list_display` attribute is set to display the `id` and `name` fields in the list view of `VegetationIndex` instances.

- **IndexPlan Model Admin (IndexPlanAdmin)**:
  - **Purpose**: The `IndexPlanAdmin` class is used to customize the Django admin interface for the `IndexPlan` model. It provides a simple history admin for tracking changes to `IndexPlan` instances.
  - **Registration**: The `IndexPlan` model is registered with the admin site using `@admin.register(IndexPlan)` decorator.
  - **Customization**: The `list_display` attribute is set to display the `id`, `value`, `culture`, and `region` fields in the list view of `IndexPlan` instances. The `list_display_links` attribute specifies that the `id` and `value` fields should be linked to the detail view.

- **Phase Model Admin (PhaseAdmin)**:
  - **Purpose**: The `PhaseAdmin` class is used to customize the Django admin interface for the `Phase` model. It provides a simple history admin for tracking changes to `Phase` instances and integrates with model translation.
  - **Registration**: The `Phase` model is registered with the admin site using `@admin.register(Phase)` decorator.
  - **Customization**: The `list_display` attribute is set to display the `id` and `name` fields in the list view of `Phase` instances. It also specifies that the `id` and `name` fields should be linked to the detail view.

These admin configurations enhance the Django admin interface for the respective models, providing features like version history tracking, translation support, and customized list views for easier management of model instances.

- 📄 [/culture_model/admin/common.py](/culture_model/admin/pasture_culture.py)

**Admin Configurations for Django Models in `culture_model`**

- **Classes Model Admin (ClassesAdmin)**:
  - **Purpose**: The `ClassesAdmin` class customizes the Django admin interface for the `Classes` model. It is used to manage classes characterized by a unique combination of a name and a description.
  - **Registration**: The `Classes` model is registered with the admin site using `@admin.register(Classes)` decorator.
  - **Customization**: The `list_display` attribute is set to display the `id` and `name` fields in the list view of `Classes` instances.

- **Subclass Model Admin (SubclassAdmin)**:
  - **Purpose**: The `SubclassAdmin` class customizes the Django admin interface for the `Subclass` model. It is used to manage subclasses associated with parent classes. Each subclass has its own unique name, description, and is related to a parent class.
  - **Registration**: The `Subclass` model is registered with the admin site using `@admin.register(Subclass)` decorator.
  - **Customization**: The `list_display` attribute is set to display the `id` and `name` fields in the list view of `Subclass` instances.

- **GroupType Model Admin (GroupTypeAdmin)**:
  - **Purpose**: The `GroupTypeAdmin` class customizes the Django admin interface for the `GroupType` model. It is used to manage group types associated with subclasses. Each group type has its own unique name, description, and is related to a specific subclass.
  - **Registration**: The `GroupType` model is registered with the admin site using `@admin.register(GroupType)` decorator.

- **RepublicanType Model Admin (RepublicanTypeAdmin)**:
  - **Purpose**: The `RepublicanTypeAdmin` class customizes the Django admin interface for the `RepublicanType` model. It is used to manage vegetation types within a Republican context. Each vegetation type has its own unique name, description, and is related to a specific group type.
  - **Registration**: The `RepublicanType` model is registered with the admin site using `@admin.register(RepublicanType)` decorator.

- **DistrictType Model Admin (DistrictTypeAdmin)**:
  - **Purpose**: The `DistrictTypeAdmin` class customizes the Django admin interface for the `DistrictType` model. It is used to manage district-specific vegetation types. Each district type is characterized by a unique combination of a vegetation type, name, description, and a specific district.
  - **Registration**: The `DistrictType` model is registered with the admin site using `@admin.register(DistrictType)` decorator.

- **PastureCulture Model Admin (PastureCultureAdmin)**:
  - **Purpose**: The `PastureCultureAdmin` class customizes the Django admin interface for the `PastureCulture` model. It is used to manage information about pasture cultures, particularly their attributes and characteristics, within specific districts and district types.
  - **Registration**: The `PastureCulture` model is registered with the admin site using `@admin.register(PastureCulture)` decorator.

These admin configurations enhance the Django admin interface for the respective models in the `culture_model`, providing features for managing classes, subclasses, group types, vegetation types, district-specific types, and pasture cultures.

## 📁 **Models folder**

Models 📋 in Django define the structure of a database table

- 📄 [/culture_model/models/decade.py](/culture_model/models/decade.py)

- **Django Model: Decade**

  - **Purpose**: The `Decade` model is designed to define and represent a specific decade or a range of years. It serves as a structured way to store information about a decade by specifying a start date and an end date to delineate the time span of that decade.

  - **Fields**:
    - `start_date`: A `DateField` that represents the starting date of the decade.
    - `end_date`: A `DateField` that represents the ending date of the decade.

  - **Meta Options**:
    - `verbose_name`: The human-readable name for a single instance of this model is set to _('Decade'), making it display as 'Decade' in the Django admin interface.
    - `verbose_name_plural`: The human-readable name for multiple instances of this model is set to _('Decades'), making it display as 'Decades' in the Django admin interface.

  - **Methods**:
    - `__str__`: This method defines the string representation of an instance of the `Decade` model. It returns a formatted string that includes the start date and end date of the decade.

  - **Example Usage**:
    - If you create an instance of `Decade` with `start_date` as '2000-01-01' and `end_date` as '2009-12-31', the `__str__` method will return "From 2000-01-01 to 2009-12-31" as the string representation of that instance.

  - **References**:
    - [Django Model Field Reference](https://docs.djangoproject.com/en/3.2/ref/models/fields/#datefield)
    - [Django Model Meta Options](https://docs.djangoproject.com/en/3.2/ref/models/options/)
    - [Django Model Methods](https://docs.djangoproject.com/en/3.2/topics/db/models/#model-methods)

- 📄 [/culture_model/models/index_plan.py](/culture_model/models/index_plan.py)

- **Django Model: IndexPlan**

  - **Purpose**: The `IndexPlan` model is designed to define and represent planned index values for specific cultural phases, decades, and regions. It serves as a structured way to store information about planned index values by specifying the culture, region, vegetation index, decade, phase, and the corresponding index value.

  - **Fields**:
    - `culture`: A foreign key to the `Culture` model, representing the culture associated with the planned index value.
    - `region`: A foreign key to the `Region` model, representing the region associated with the planned index value.
    - `index`: A foreign key to the `VegetationIndex` model, representing the vegetation index associated with the planned index value.
    - `decade`: A foreign key to the `Decade` model, representing the decade associated with the planned index value.
    - `phase`: A foreign key to the `Phase` model, representing the cultural phase associated with the planned index value.
    - `value`: A `DecimalField` that stores the index value, with a maximum of 5 digits and 3 decimal places, defaulting to 0.

  - **Meta Options**:
    - `verbose_name`: The human-readable name for a single instance of this model is set to _('Planned Index Value'), making it display as 'Planned Index Value' in the Django admin interface.
    - `verbose_name_plural`: The human-readable name for multiple instances of this model is set to _('Planned Index Values'), making it display as 'Planned Index Values' in the Django admin interface.

  - **Methods**:
    - `__str__`: This method defines the string representation of an instance of the `IndexPlan` model. It returns a formatted string that includes the index value.

  - **Example Usage**:
    - If you create an instance of `IndexPlan` with a `value` of 0.75, the `__str__` method will return "Index Value (0.75)" as the string representation of that instance.

  - **References**:
    - [Django Model Field Reference](https://docs.djangoproject.com/en/3.2/ref/models/fields/#decimalfield)
    - [Django Model Meta Options](https://docs.djangoproject.com/en/3.2/ref/models/options/)
    - [Django Model Methods](https://docs.djangoproject.com/en/3.2/topics/db/models/#model-methods)

- 📄 [/culture_model/models/pasture_culture.py](/culture_model/models/pasture_culture.py)

- **Django Model: Classes**

  - **Purpose**: The `Classes` model defines and represents classes, each characterized by a unique combination of a name and a description. It's used to organize and manage different classes within your application.

  - **Fields**:
    - `name`: A character field with a maximum length of 20 characters, representing the name of the class.
    - `description`: A text field that stores the description of the class.

  - **Meta Options**:
    - `unique_together`: Specifies that the combination of `name` and `description` must be unique.
    - `verbose_name`: The human-readable name for a single instance of this model is set to _('Class'), making it display as 'Class' in the Django admin interface.
    - `verbose_name_plural`: The human-readable name for multiple instances of this model is set to _('Classes'), making it display as 'Classes' in the Django admin interface.

- **Django Model: Subclass**

  - **Purpose**: The `Subclass` model defines and represents subclasses associated with a parent class (Classes). Each subclass has its unique name, description, and is related to a parent class.

  - **Fields**:
    - `classes`: A foreign key to the `Classes` model, representing the parent class associated with the subclass.
    - `name`: A character field with a maximum length of 20 characters, representing the name of the subclass.
    - `description`: A text field that stores the description of the subclass.

  - **Meta Options**:
    - `unique_together`: Specifies that the combination of `name`, `description`, and `classes` must be unique.
    - `verbose_name`: The human-readable name for a single instance of this model is set to _('Subclass'), making it display as 'Subclass' in the Django admin interface.
    - `verbose_name_plural`: The human-readable name for multiple instances of this model is set to _('Subclasses'), making it display as 'Subclasses' in the Django admin interface.

- **Django Model: GroupType**

  - **Purpose**: The `GroupType` model defines and represents group types associated with subclasses. Each group type has its unique name, description, and is related to a specific subclass.

  - **Fields**:
    - `subclass`: A foreign key to the `Subclass` model, representing the subclass associated with the group type.
    - `name`: A character field with a maximum length of 20 characters, representing the name of the group type.
    - `description`: A text field that stores the description of the group type.

  - **Meta Options**:
    - `unique_together`: Specifies that the combination of `name`, `description`, and `subclass` must be unique.
    - `verbose_name`: The human-readable name for a single instance of this model is set to _('Group Type'), making it display as 'Group Type' in the Django admin interface.
    - `verbose_name_plural`: The human-readable name for multiple instances of this model is set to _('Group Types'), making it display as 'Group Types' in the Django admin interface.

- **Django Model: RepublicanType**

  - **Purpose**: The `RepublicanType` model defines and represents vegetation types within a Republican context. Each vegetation type has its unique name, description, and is related to a specific group type.

  - **Fields**:
    - `type_group`: A foreign key to the `GroupType` model, representing the group type associated with the vegetation type.
    - `name`: A character field with a maximum length of 20 characters, representing the name of the vegetation type.
    - `description`: A text field that stores the description of the vegetation type.

  - **Meta Options**:
    - `unique_together`: Specifies that the combination of `name`, `description`, and `type_group` must be unique.
    - `verbose_name`: The human-readable name for a single instance of this model is set to _('Vegetation Type'), making it display as 'Vegetation Type' in the Django admin interface.
    - `verbose_name_plural`: The human-readable name for multiple instances of this model is set to _('Vegetation Types'), making it display as 'Vegetation Types' in the Django admin interface.

- **Django Model: DistrictType**

  - **Purpose**: The `DistrictType` model defines and represents district-specific vegetation types. Each district type is characterized by a unique combination of a vegetation type, name, description, and a specific district.

  - **Fields**:
    - `type_group`: A foreign key to the `RepublicanType` model, representing the vegetation type associated with the district type.
    - `name`: A character field with a maximum length of 20 characters, representing the name of the district type.
    - `description`: A text field that stores the description of the district type.
    - `district`: A foreign key to the `District` model, representing the specific district associated with the district type.

  - **Meta Options**:
    - `unique_together`: Specifies that the combination of `type_group`, `name`, `description`, and `district` must be unique.
    - `verbose_name`: The human-readable name for a single instance of this model is set to _('District Type'), making it display as 'District Type' in the Django admin interface.
    - `verbose_name_plural`: The human-readable name for multiple instances of this model is set to _('District Types'), making it display as 'District Types' in the Django admin interface.

- **Django Model: PastureCulture**

  - **Purpose**: The `PastureCulture` model defines and represents information about pasture cultures, including their attributes and characteristics, within specific districts and district types.

  - **Fields**:
    - `district_type`: A foreign key to the `DistrictType` model, representing the district type associated with the pasture culture.
    - `name`: A character field with a maximum length of 255 characters, representing the name of the pasture culture.
    - `coefficient_to_productivity`: A decimal field with a maximum of 4 digits and 2 decimal places, storing the productivity coefficient of the pasture culture.
    - `content_of_feed`: A decimal field with a maximum of 4 digits and 2 decimal places, storing the feed content of the pasture culture.
    - `district`: A foreign key to the `District` model, representing the specific district associated with the pasture culture.
    - `veg_period`: A foreign key to the `Phase` model, representing the vegetation period associated with the pasture culture.

  - **Meta Options**:
    - `unique_together`: Specifies that the combination of `district_type`, `name`, `coefficient_to_productivity`, `content_of_feed`, and `district` must be unique.
    - `verbose_name`: The human-readable name for a single instance of this model is set to _('Pasture Culture'), making it display as 'Pasture Culture' in the Django admin interface.
    - `verbose_name_plural`: The human-readable name for multiple instances of this model is set to _('Pasture Cultures'), making it display as 'Pasture Cultures' in the Django admin interface.

- 📄 [/culture_model/models/phase.py](/culture_model/models/phase.py)

- **Django Model: Phase**

  - **Purpose**: The `Phase` model serves the purpose of defining and representing information about development phases. It is used to categorize and describe different phases of development within a system or process.

  - **Fields**:
    - `name`: A character field with a maximum length of 125 characters, representing the name of the development phase.

  - **Meta Options**:
    - `verbose_name`: The human-readable name for a single instance of this model is set to _('Development Phase'), making it display as 'Development Phase' in the Django admin interface.
    - `verbose_name_plural`: The human-readable name for multiple instances of this model is set to _('Development Phases'), making it display as 'Development Phases' in the Django admin interface.

  - **Methods**:
    - `__str__(self)`: This method returns the name of the development phase as its string representation.

This model is used to categorize and manage different development phases within your Django application. It provides a structured way to represent and organize information about various phases in a system or process.

- 📄 [/culture_model/models/vegetation_index.py](/culture_model/models/vegetation_index.py)

- **Django Model: VegetationIndex**

  - **Purpose**: The `VegetationIndex` model serves the purpose of defining and representing information about various vegetation indices. It is used to categorize and describe different types of vegetation indices that may be used in applications related to agriculture, environmental monitoring, and more.

  - **Fields**:
    - `name`: A character field with a maximum length of 125 characters, representing the name of the vegetation index.
    - `description`: A text field used to provide a detailed description of the vegetation index.

  - **Meta Options**:
    - `verbose_name`: The human-readable name for a single instance of this model is set to _('Vegetation Index'), making it display as 'Vegetation Index' in the Django admin interface.
    - `verbose_name_plural`: The human-readable name for multiple instances of this model is set to _('Vegetation Indices'), making it display as 'Vegetation Indices' in the Django admin interface.

  - **Methods**:
    - `__str__(self)`: This method returns the name of the vegetation index as its string representation.

This model provides a structured way to categorize and manage information about different vegetation indices. It allows users to define and describe various types of vegetation indices used in agricultural, environmental, or related applications.

## 📁 **Serializers folder**

Serializers 🔄 in Django convert data for web APIs.

- 📄 [/culture_model/serializers/index.py](/culture_model/serializers/index.py)

**Serializer for VegetationIndex Model (IndexSerializer)**

- **Purpose**: The `IndexSerializer` class is a serializer used in Django Rest Framework (DRF) to transform instances of the `VegetationIndex` model into a serialized format, typically JSON, that can be easily rendered into content suitable for client applications. This serializer is responsible for controlling which fields of the `VegetationIndex` model are included or excluded when data is serialized.
  
- **Meta Class**:
  - `model = VegetationIndex`: Specifies the Django model associated with this serializer, which is `VegetationIndex` in this case.
  - `exclude = ('name', 'description')`: Defines a list of fields from the `VegetationIndex` model that should be excluded when serializing data. In this case, the `name` and `description` fields will not be included in the serialized output.

This serializer simplifies the process of converting `VegetationIndex` model instances into a format that can be easily consumed by client applications while excluding specific fields as per the `exclude` attribute.

## 📁 **Views folder**

Views 👀 in Django control how data is displayed and processed.

- 📄 [/culture_model/views/veg_indexes.py](/culture_model/views/veg_indexes.py)

**API View for Retrieving Vegetation Indexes (VegIndexAPIView)**

- **Purpose**: The `VegIndexAPIView` class is an API view in Django Rest Framework (DRF) designed to retrieve a list of all vegetation indexes from the database and present them as a serialized response. This API view allows clients to fetch information about vegetation indexes.

- **Methods**:
  - `get(self, request, *args, **kwargs)`: This method is used to handle HTTP GET requests made to the API endpoint associated with this view. It retrieves all vegetation indexes from the database, orders them by their 'id' field, and serializes the data using the `IndexSerializer`. If there are no vegetation indexes in the database, it returns a response with a 400 status code and an error message. Otherwise, it returns a response with a 200 status code and the serialized data.

- **Swagger Documentation**:
  - `@swagger_auto_schema(...)`: This decorator is used to provide Swagger documentation for the 'get' method. It includes information such as the operation summary and possible responses. For a successful response (status code 200), it specifies that the response should be serialized using `IndexSerializer`. For an error response (status code 400), it provides an error message.

This API view simplifies the process of retrieving a list of vegetation indexes from the database and presenting them in a structured format, making it accessible to client applications. The Swagger documentation ensures that developers understand how to interact with this endpoint.

## 📁 **Tests folder**

The "tests" folder ensures the app's code reliability.

- 📄 Files:
  - [factories.py](/culture_model/tests/factories.py)
  - [tests.py](/culture_model/tests/tests.py)

## 📄 **translation.py**

[Translate models 🌐.](/culture_model/translation.py)

## 📄 **urls.py**

[It's where the url's configurations 🛠️ are stored.](/culture_model/urls.py)
