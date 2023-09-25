# 📂 **Account App**

```
📁 **auditlog**
│
├── 📁 management
│   └── 📁 commands
│       ├── 📄 auditlogflush.py
│       └── 📄 auditlogmigratejson.py
│
├── 📄 admin.py
├── 📄 apps.py
├── 📄 cid.py
├── 📄 conf.py
├── 📄 context.py
├── 📄 diff.py
├── 📄 filters.py
├── 📄 middleware.py
├── 📄 mixins.py
├── 📄 models.py
├── 📄 receivers.py
├── 📄 registry.py
└── 📄 signals.py
```

## 📁 **Management folder**

Management commands - commands executed from the command line using the manage.py script.

- 📄 [/auditlog/management/commands/auditlogflush.py](/auditlog/management/commands/auditlogflush.py)

- **Command**: `DeleteLogEntriesCommand`

  - **Description**: This Django management command is used to delete log entries from the database, specifically using the `auditlog` app. It allows for the removal of log entries created by the auditlog app.

  - **Options**:
    - `-y` or `--yes`: An optional flag to bypass the confirmation prompt and proceed with deletion.
    - `-b` or `--before-date`: An optional flag to specify a date (in ISO 8601 format) before which log entries should be deleted.

  - **Functionality**:
    - If the `--yes` flag is not provided, the command will prompt the user for confirmation before deleting log entries.
    - The `-b` or `--before-date` flag allows filtering log entries based on a specified date.
    - Once confirmed, the command proceeds to delete log entries, and the number of deleted entries is displayed as output.

  - **Usage**:
    - To delete all log entries: `python manage.py delete_log_entries`
    - To delete log entries before a specific date: `python manage.py delete_log_entries -b YYYY-MM-DD`
    - To delete all log entries without confirmation: `python manage.py delete_log_entries -y`

  - **Note**: Deleting log entries is an irreversible action and should be used with caution.

- **Imported Modules**: The command imports necessary modules, including `datetime` and the `LogEntry` model from the `auditlog` app.

This command provides a convenient way to manage and clean log entries, especially when working with auditing and logging features in Django applications. Use it to maintain a clean and manageable log history.

- 📄 [/auditlog/management/commands/auditlogmigratejson.py](/auditlog/management/commands/auditlogmigratejson.py)

- **Command**: `MigrateLogChangesCommand`

  - **Description**: This Django management command is used to migrate changes from the `changes_text` field to the `changes` field in the `auditlog_logentry` table, effectively changing the data format from text to JSON. The migration can be performed using either Django operations (`bulk_update`) or native database operations, depending on the provided options.

  - **Options**:
    - `-d` or `--database`: An optional flag to specify the database for native operations. Supported databases include PostgreSQL, MySQL, and Oracle.
    - `-b` or `--batch-size`: An optional flag to split the migration into multiple batches when using Django operations. If set to 0, no batching will be done.

  - **Functionality**:
    - The command checks for log entries that need migration (where `changes_text` is not empty and `changes` is empty).
    - Depending on the options chosen, the command migrates the data using Django's `bulk_update` or native database operations.
    - The migration process updates the `changes` field with JSON data parsed from the `changes_text` field.
    - The command also supports batching for large datasets, making it more efficient.
    - After migration, it checks the logs again and provides feedback on the status.

  - **Usage**:
    - To migrate log changes using Django operations: `python manage.py migrate_log_changes`
    - To migrate log changes using native database operations (PostgreSQL only): `python manage.py migrate_log_changes -d postgres`
    - To control batch size for Django operations: `python manage.py migrate_log_changes -b 500`
    - To use native database operations, run the command without specifying a database: `python manage.py migrate_log_changes`

  - **Note**: This command is useful for migrating log data from text to JSON format. It's important to choose the appropriate method (Django or native) based on your database and requirements.

- **Imported Modules**: The command imports necessary modules, including `json`, `ceil`, and `settings`, along with the `LogEntry` model from the `auditlog` app.

Use this command to efficiently migrate log data and update the data format as needed in your Django application.

## [📄 **admin.py**](/auditlog/admin.py)

- **Admin Configuration for LogEntry Model**

  - **Description**: This code registers the `LogEntry` model in the Django admin interface, providing an admin panel for viewing and managing audit log entries. It includes various configurations for list views, search fields, filters, readonly fields, fieldsets, and permissions.

  - **Configuration**:
    - `list_select_related`: Selects related fields like content type and actor in a single query to optimize performance.
    - `list_display`: Defines columns to display in the admin list view, including creation timestamp, resource URL, action, and user URL.
    - `search_fields`: Configures search fields for filtering log entries by timestamp, object representation, changes, actor's first name, last name, and username.
    - `list_filter`: Sets filters for the admin list view, allowing filtering by action, resource type, and actor.
    - `readonly_fields`: Specifies fields as readonly in the admin view.
    - `fieldsets`: Organizes fields into two sections in the admin form: "Changes" and other fields.
    - Permission Overrides: Disables add, change, and delete permissions in the admin interface to prevent modification of log entries.
    - `get_queryset`: Overrides the default queryset to include request information for audit log entries.

  - **Usage**: This code should be placed in your Django project's admin.py file to enable the administration of log entries.

- **Imported Modules and Classes**: The code imports necessary modules and classes from Django, including the `admin` module, `get_user_model` function, and `gettext_lazy` for translation. It also imports relevant components from the `auditlog` app, such as filters, mixins, and the `LogEntry` model.

Feel free to use this description as needed. If you have any further requests or modifications, please let me know!

## [📄 **cid.py**](/auditlog/cid.py)

- **Context Variable and Correlation ID Management**

  - **Description**: This code defines a set of functions and mechanisms for managing correlation IDs (CIDs) in a Django application. Correlation IDs are used to track requests and events across services, helping with debugging and tracing in distributed systems.

  - **Code Components**:
    - `correlation_id`: A `ContextVar` instance used to store and manage the correlation ID for the current request context.
    - `set_cid(request)`: A function that sets the correlation ID (CID) based on the request. It checks the presence of a specified header (configured in `settings.AUDITLOG_CID_HEADER`) in the request's headers or `META` dictionary. If the header is found, the CID is set to its value; otherwise, it's set to `None`.
    - `_get_cid()`: An internal function that retrieves the CID from the `correlation_id` context variable.
    - `get_cid()`: A function that gets the CID based on the configured getter method defined in `settings.AUDITLOG_CID_GETTER`. The getter can be `None` (default), a callable function, or a string representing an importable function. It provides flexibility for custom CID retrieval logic, either dependent on `set_cid` or independent.

  - **Usage**: This code should be integrated into a Django project for managing and retrieving correlation IDs. The settings `AUDITLOG_CID_HEADER` and `AUDITLOG_CID_GETTER` can be configured to customize CID behavior. For instance, you can use custom getters for CID retrieval, depending on your application's requirements.

- **ContextVar**: The code utilizes the `ContextVar` class from the `contextvars` module, which provides a context-local variable for managing the correlation ID within a request context.

- **Header-Based CID Retrieval**: The `set_cid` function retrieves the CID from the request's headers or `META` dictionary based on the configured header (in `settings.AUDITLOG_CID_HEADER`). If the header is found, the CID is set; otherwise, it defaults to `None`.

- **Dynamic CID Getter**: The `get_cid` function dynamically selects the CID getter method based on the `settings.AUDITLOG_CID_GETTER`. It can be configured to use a custom getter function or the default `_get_cid` function.

- **Customization**: Developers can customize CID handling by specifying custom getter functions or relying on the default mechanism. The flexibility allows for integration with various CID-generation strategies.

Feel free to use this description as needed. If you have any further requests or modifications, please let me know!

## [📄 **conf.py**](/auditlog/conf.py)

- **Django Audit Log Settings**

  - **Description**: This code defines various settings that configure the behavior of the Django audit log library. These settings allow developers to customize the auditing process according to their project requirements.

  - **Settings Overview**:

    - `AUDITLOG_INCLUDE_ALL_MODELS`: A boolean setting that, when set to `True`, registers all models for auditing by default. Developers can set this in their project settings to control whether all models should be audited.

    - `AUDITLOG_EXCLUDE_TRACKING_MODELS`: A tuple setting that allows developers to exclude specific models from the audit log registration process. Models listed in this setting will not be audited even if `AUDITLOG_INCLUDE_ALL_MODELS` is `True`.

    - `AUDITLOG_INCLUDE_TRACKING_MODELS`: A tuple setting for explicitly registering and configuring auditing behavior for specific models. Developers can list models in this setting to ensure they are audited, along with additional customization.

    - `AUDITLOG_EXCLUDE_TRACKING_FIELDS`: A tuple setting that excludes specific fields across all models from being audited. Fields listed in this setting will not generate audit log entries.

    - `AUDITLOG_DISABLE_ON_RAW_SAVE`: A boolean setting that, when set to `True`, disables audit logging during raw save operations to avoid unnecessary logging of imports and similar activities.

    - `AUDITLOG_CID_HEADER`: A setting specifying the header name used for correlation IDs (CIDs) in HTTP requests. Developers can customize this header name as needed.

    - `AUDITLOG_CID_GETTER`: A setting defining the method for retrieving correlation IDs (CIDs). Developers can specify a custom function or use the default method (`None`) for CID retrieval.

    - `AUDITLOG_TWO_STEP_MIGRATION`: A boolean setting that controls whether two-step migration should be used during the migration process.

    - `AUDITLOG_USE_TEXT_CHANGES_IF_JSON_IS_NOT_PRESENT`: A boolean setting that determines whether text changes should be used if JSON changes are not available.

  - **Usage**: Developers can configure these settings in their Django project's settings module to tailor the audit logging behavior according to their specific use cases and preferences. These settings provide flexibility for controlling which models are audited, customizing field exclusions, handling CID headers, and more.

- **Customization**: By adjusting these settings, developers can fine-tune the behavior of the Django audit log library to align with their project's auditing requirements and constraints.

Feel free to use this description as needed. If you have any further requests or modifications, please let me know!

## [📄 **context.py**](/auditlog/context.py)

- **Django Audit Log Context Managers**

  - **Description**: This code defines context managers for managing the actor (user) assignment and disabling of audit logging within Django applications. These context managers facilitate the auditing process and allow developers to control when and how actors are assigned to audit log entries.

  - **Context Managers Overview**:

    - `set_actor`: This context manager is used to attach a user (actor) to signal receivers within a specific context. It connects a signal receiver for automatic logging and allows developers to specify the actor and remote address for audit log entries.

    - `disable_auditlog`: This context manager is used to temporarily disable audit logging within a specific context. It sets a flag to disable audit logging and can be used to skip audit log entries for certain operations.

  - **Usage**: Developers can use these context managers in their Django application code to:

    - Set the actor (user) for audit log entries within a specific context, ensuring that log entries are associated with the correct user.

    - Temporarily disable audit logging for specific operations or sections of code by using the `disable_auditlog` context manager.

  - **Customization**: Developers can customize these context managers and integrate them into their Django application code to control the behavior of audit logging based on their project's requirements.

- **Examples**:

  1. **Setting the Actor (User) Context**:

     ```python
     with set_actor(user=current_user, remote_addr=request.META.get('REMOTE_ADDR')):
         # Perform operations requiring actor assignment for audit logs
         # Audit log entries will be associated with 'current_user'
     ```

  2. **Disabling Audit Logging Temporarily**:

     ```python
     with disable_auditlog():
         # Perform operations where audit logging is temporarily disabled
         # Audit log entries will be skipped during this context
     ```

Feel free to use this description as needed. If you have any further requests or modifications, please let me know!

## [📄 **diff.py**](/auditlog/diff.py)

- **Django Auditlog Field Tracking and Model Difference Calculation**

  - **Description**: This code provides utility functions for tracking model fields and calculating differences between two model instances. These functions are used within the Django Auditlog library to determine changes made to model instances and log them accordingly.

  - **Functions Overview**:

    - `track_field(field)`: Determines whether a given field should be tracked by Auditlog. It excludes many-to-many relations and relations to the Auditlog `LogEntry` model.

    - `get_fields_in_model(instance)`: Retrieves the list of fields in a given model instance, excluding many-to-many fields.

    - `get_field_value(obj, field)`: Gets the value of a specific field in a model instance. Handles various field types, including DateTimeFields and JSONFields.

    - `mask_str(value)`: Masks the first half of a string value to remove sensitive data, used for masking field values.

    - `model_instance_diff(old, new, fields_to_check=None)`: Calculates the differences between two model instances. Returns a dictionary with changed field names as keys and a two-tuple of old and new field values as values.

  - **Usage**: Developers can use these functions within their Django Auditlog customizations to:

    - Determine which fields should be tracked for changes in model instances.

    - Retrieve a list of fields in a model instance for further processing.

    - Get the value of a specific field in a model instance for comparison.

    - Mask sensitive data in field values using the `mask_str` function.

    - Calculate and retrieve the differences between two model instances using the `model_instance_diff` function.

  - **Customization**: These utility functions can be customized or integrated into Django applications as needed for tracking, logging, and auditing changes to model instances.

- **Examples**:

  1. **Tracking Fields in a Model**:

     ```python
     # Check if a field should be tracked by Auditlog
     should_track = track_field(field)
     ```

  2. **Retrieving Model Fields in an Instance**:

     ```python
     # Get a list of fields in a model instance
     fields_list = get_fields_in_model(instance)
     ```

  3. **Getting Field Values in an Instance**:

     ```python
     # Get the value of a specific field in a model instance
     field_value = get_field_value(obj, field)
     ```

  4. **Calculating Model Instance Differences**:

     ```python
     # Calculate differences between old and new model instances
     differences = model_instance_diff(old_instance, new_instance, fields_to_check=None)
     ```

Feel free to use this description as needed. If you have any further requests or modifications, please let me know!


## [📄 **filters.py**](/auditlog/filters.py)

- **Django Custom Admin Filters**

  - **Description**: This code defines two custom admin filters for use in the Django admin interface. These filters allow administrators to filter records in the admin list view based on specific criteria.

  - **ResourceTypeFilter**:

    - **Title**: "Tables"

    - **Parameter Name**: "resource_type"

    - **Description**: This filter provides a dropdown list of resource types (content types) to filter records based on the associated content type. It retrieves the content type names from the database and displays them in the filter options.

    - **Methods**:

      - `lookups(self, request, model_admin)`: Returns a list of lookup options for the filter, consisting of tuples containing content type IDs and names.

      - `queryset(self, request, queryset)`: Filters the queryset based on the selected content type (resource type).

  - **CIDFilter**:

    - **Title**: "Correlation ID"

    - **Parameter Name**: "cid"

    - **Description**: This filter allows administrators to filter records based on a correlation ID (CID). Unlike the ResourceTypeFilter, this filter does not provide predefined options and is intended for manually entering a CID value.

    - **Methods**:

      - `lookups(self, request, model_admin)`: Returns an empty list of lookups since CIDFilter does not have predefined options.

      - `has_output(self)`: Indicates that the filter has an output.

      - `queryset(self, request, queryset)`: Filters the queryset based on the selected CID.

  - **Usage**: These custom admin filters can be added to Django admin views to enhance the filtering capabilities of the admin interface. ResourceTypeFilter is used for filtering records by resource type (content type), while CIDFilter is used for filtering records by correlation ID.

  - **Examples**:

    1. **Using ResourceTypeFilter**:

       ```python
       # In the admin class, add ResourceTypeFilter to the list_filter attribute
       list_filter = [ResourceTypeFilter]
       ```

    2. **Using CIDFilter**:

       ```python
       # In the admin class, add CIDFilter to the list_filter attribute
       list_filter = [CIDFilter]
       ```

Feel free to use this description as needed. If you have any further requests or modifications, please let me know!


## [📄 **Middleware module**](/auditlog/middleware.py)

- **Django Auditlog Middleware**

  - **Description**: This Django middleware is designed to associate the current user and remote address with log items generated during the request-response cycle. It achieves this by currying the signal receiver function with the user from the request (or None if the user is not authenticated) and the remote address of the client.

  - **Methods**:

    - `__init__(self, get_response=None)`: Initializes the middleware instance. It takes an optional `get_response` parameter, which is a callable that handles the request.

    - `_get_remote_addr(request)`: A static method that retrieves the remote address of the client making the request. It takes into account the presence of proxy servers and extracts the original remote address.

    - `_get_actor(request)`: A static method that retrieves the user associated with the request. If a user is authenticated, it returns the user instance; otherwise, it returns `None`.

    - `__call__(self, request)`: The main method of the middleware, called for each incoming request. It sets the correlation ID (CID) using the `set_cid` function, and then uses a context manager (`set_actor`) to associate the user and remote address with log items generated during the request-response cycle.

  - **Usage**: This middleware is added to the Django application's middleware stack to automatically capture the user and remote address for log entries generated by the auditlog package during request processing. By associating this information with log entries, it helps in tracking and auditing actions performed by users.

  - **Examples**:

    1. **Middleware Configuration**:

       To use this middleware, add it to the `MIDDLEWARE` setting in your Django project's settings file:

       ```python
       MIDDLEWARE = [
           # ...
           'yourapp.middleware.AuditlogMiddleware',  # Replace with the actual import path
           # ...
       ]
       ```

  - **Note**: This middleware relies on the `auditlog.cid.set_cid` function to set the correlation ID (CID) for the request. Ensure that the `set_cid` function is correctly configured and available in your project.

Feel free to use this description as needed. If you have any further requests or modifications, please let me know!

## [📄 **Mixins module**](/auditlog/mixins.py)

- **Django Auditlog Mixins for Admin and Object Access Logging**

  - **Description**: These Django mixins are designed to enhance the admin view of log entries and to track access to objects using the Django Auditlog package.

  - **`LogEntryAdminMixin`**:

    - **Methods**:

      - `created(self, obj)`: Displays the creation timestamp of the log entry in the user's local time.

      - `user_url(self, obj)`: Displays a link to the user's admin change page or "Admin Panel" if no user is associated with the log entry.

      - `resource_url(self, obj)`: Displays a link to the admin change page of the associated resource (object).

      - `msg_short(self, obj)`: Displays a summary of changes made in the log entry, including the number of changes and affected fields.

      - `msg(self, obj)`: Displays detailed changes made in the log entry, including atomic changes and many-to-many relationship changes.

      - `cid_url(self, obj)`: Displays a link to filter records with the same correlation ID.

      - `_format_header(self, *labels)`: Formats an HTML table header row.

      - `_format_line(self, *values)`: Formats an HTML table row.

      - `field_verbose_name(self, obj, field_name)`: Retrieves the verbose name of a field in a model or from a mapping dictionary.

      - `_add_query_parameter(self, key, value)`: Adds a query parameter to the current request's URL.

    - **Usage**: The `LogEntryAdminMixin` is intended to be used in conjunction with Django admin views to enhance the display of log entries. It provides methods for displaying log entry details, including changes, timestamps, associated users, and resource URLs.

  - **`LogAccessMixin`**:

    - **Methods**:

      - `render_to_response(self, context, **response_kwargs)`: Overrides the `render_to_response` method to track access to objects. When this mixin is used, it sends an access signal when an object is accessed via the view.

    - **Usage**: The `LogAccessMixin` is intended to be used with Django views to track access to objects. When an object is accessed via a view that uses this mixin, it sends an access signal, which can be used for auditing and logging purposes.

  - **Examples**:

    1. **Usage of `LogEntryAdminMixin`**:

       To enhance the admin view of log entries, you can create an admin class for the `LogEntry` model and use `LogEntryAdminMixin` in it:

       ```python
       @admin.register(LogEntry)
       class LogEntryAdmin(admin.ModelAdmin, LogEntryAdminMixin):
           # Your admin configuration here
       ```

    2. **Usage of `LogAccessMixin`**:

       To track access to objects, you can create a view class and use `LogAccessMixin` in it. When an object is accessed via this view, an access signal will be sent:

       ```python
       class MyDetailView(DetailView, LogAccessMixin):
           # Your view configuration here
       ```

  - **Note**: These mixins are designed to work seamlessly with the Django Auditlog package and enhance the auditing and admin capabilities of a Django project.

Feel free to use this description as needed. If you have any further requests or modifications, please let me know!


## [📄 **models.py**](/auditlog/models.py)

- **Django Auditlog Manager, Model, and Field for Auditing and Logging**

  - **Description**: This code defines a custom manager (`LogEntryManager`), a model (`LogEntry`), and a generic relation field (`AuditlogHistoryField`) for auditing and logging changes to Django models. These components are part of the Django Auditlog package.

  - **`LogEntryManager`**:

    - **Methods**:

      - `log_create(self, instance, force_log=False, **kwargs)`: Helper method to create a new log entry for a model instance. This method automatically populates some fields and creates a log entry if changes exist or if forced.

      - `log_m2m_changes(self, changed_queryset, instance, operation, field_name, **kwargs)`: Creates a new log entry for many-to-many relationship changes.

      - `get_for_object(self, instance)`: Gets log entries for a specific model instance.

      - `get_for_objects(self, queryset)`: Gets log entries for objects in a queryset.

      - `get_for_model(self, model)`: Gets log entries for all objects of a specified model type.

      - `_get_pk_value(self, instance)`: Gets the primary key field value for a model instance.

      - `_get_serialized_data_or_none(self, instance)`: Gets serialized data for a model instance.

      - `_get_copy_with_python_typed_fields(self, instance)`: Creates a copy of the instance and coerces field types to Python types.

      - `_get_applicable_model_fields(self, instance, model_fields)`: Gets applicable model fields for serialization.

      - `_mask_serialized_fields(self, data, mask_fields)`: Masks serialized fields for security or privacy.

  - **`LogEntry` Model**:

    - **Attributes**:

      - `Action`: An inner class that defines different actions (CREATE, UPDATE, DELETE, ACCESS) for logging.

    - **Fields**:

      - `content_type`: ForeignKey to ContentType.

      - `object_pk`: CharField for the identifier of the logged object.

      - `object_id`: BigIntegerField for the numeric primary key of the logged object.

      - `object_repr`: TextField for the textual representation of the logged object.

      - `serialized_data`: JSONField for storing serialized data of the object.

      - `action`: PositiveSmallIntegerField for the action performed (CREATE, UPDATE, DELETE, ACCESS).

      - `changes_text`: TextField for storing textual change details.

      - `changes`: JSONField for storing detailed change information.

      - `actor`: ForeignKey to the User model for the user who initiated the change.

      - `cid`: CharField for storing a correlation ID.

      - `remote_addr`: GenericIPAddressField for the remote address.

      - `timestamp`: DateTimeField for the timestamp of the log entry.

      - `additional_data`: JSONField for additional data related to the log entry.

    - **Methods**:

      - `changes_dict`: Property that returns the changes recorded in this log entry as a dictionary.

      - `changes_str`: Property that returns a formatted string of the changes recorded in this log entry.

      - `changes_display_dict`: Property that returns changes intended for display to users as a dictionary.

  - **`AuditlogHistoryField`**:

    - **Description**: A generic relation field used to link log entries to model instances. Allows auditing and accessing change history for objects.

    - **Attributes**:

      - `pk_indexable`: Whether the primary key for this model is not an integer or long (default: True).

      - `delete_related`: Whether to cascade-delete related objects when the parent object is deleted (default: True).

  - **`changes_func`**:

    - **Description**: A function that determines how changes are retrieved from a `LogEntry`. Depending on settings, it can retrieve changes as JSON or text. This function is used in the `LogEntry` model to fetch changes.

  - **`_changes_func()`**:

    - **Description**: Internal function that defines the logic for `changes_func` based on settings.

  - **Usage**: These components are used to track and log changes to model instances, providing auditing and history tracking capabilities. `LogEntryManager` provides methods for creating and querying log entries, while the `LogEntry` model stores the details of each log entry. `AuditlogHistoryField` is used to link log entries to model instances.

Feel free to use this description as needed. If you have any further requests or modifications, please let me know!

## [📄 **receivers.py**](/auditlog/receivers.py)

- **Django Auditlog Signal Handlers**

  - **Description**: This code defines signal handlers for auditing and logging changes to Django models using the Django Auditlog package. The signal handlers handle model create, update, delete, and access events and create log entries accordingly.

  - **Signal Handlers**:

    - `log_create(sender, instance, created, **kwargs)`: Signal receiver that creates a log entry when a model instance is first saved to the database. It is called when a model instance is created.

    - `log_update(sender, instance, **kwargs)`: Signal receiver that creates a log entry when a model instance is changed and saved to the database. It is called when a model instance is updated.

    - `log_delete(sender, instance, **kwargs)`: Signal receiver that creates a log entry when a model instance is deleted from the database. It is called when a model instance is deleted.

    - `log_access(sender, instance, **kwargs)`: Signal receiver that creates a log entry when a model instance is accessed in an `AccessLogDetailView`. It is called when a model instance is accessed.

  - **Helper Functions**:

    - `_create_log_entry(action, instance, sender, diff_old, diff_new, fields_to_check=None, force_log=False)`: Internal function that creates a log entry based on the provided action and instance. It calculates the changes between old and new instances, and creates a log entry if changes exist. This function is used by the signal handlers.

    - `make_log_m2m_changes(field_name)`: Returns a signal handler for many-to-many (m2m) relationship changes with the specified `field_name`.

  - **Decorators**:

    - `check_disable(signal_handler)`: Decorator that checks whether auditing is disabled (based on thread-local or raw save settings) before invoking the wrapped signal handler.

  - **Usage**: These signal handlers are used to trigger log entries creation when specific model events occur, such as create, update, delete, and access. The `_create_log_entry` function is responsible for creating log entries, and the `make_log_m2m_changes` function returns a handler for m2m relationship changes.

Feel free to use this description as needed. If you have any further requests or modifications, please let me know!

## [📄 **registry.py**](/auditlog/registry.py)

- **Django Auditlog Model Registry and Configuration**

  - **Description**: This code defines a registry for models that use the Django Auditlog package to track changes. The `AuditlogModelRegistry` class allows you to register models, configure their tracking options, and control which models are audited for changes. Additionally, it provides methods to register models based on settings and exclude certain models from tracking.

  - **Attributes**:

    - `_registry`: A dictionary that stores registered models along with their tracking options.
    - `_signals`: A dictionary that maps Django signals (e.g., `post_save`, `pre_save`) to corresponding signal handlers for auditing actions.
    - `_m2m_signals`: A dictionary that stores many-to-many (m2m) signal handlers for auditing m2m relationship changes.
    - `_m2m`: A boolean indicating whether to audit m2m relationship changes.

  - **Methods**:

    - `register(model=None, include_fields=None, exclude_fields=None, mapping_fields=None, mask_fields=None, m2m_fields=None, serialize_data=False, serialize_kwargs=None, serialize_auditlog_fields_only=False)`: Register a model with auditlog and specify tracking options. You can define which fields to include, exclude, map, or mask. You can also configure m2m field tracking and serialization options.

    - `contains(model)`: Check if a model is registered with auditlog.

    - `unregister(model)`: Unregister a model from auditlog, removing it from auditing.

    - `get_models()`: Get a list of all registered models.

    - `get_model_fields(model)`: Get the tracking options and field configurations for a specific model.

    - `get_serialize_options(model)`: Get the serialization options for a specific model.

    - `_connect_signals(model)`: Connect auditlog signals to a registered model for tracking changes.

    - `_disconnect_signals(model)`: Disconnect auditlog signals from a registered model when unregistering it.

    - `_dispatch_uid(signal, receiver)`: Generate a unique identifier for a combination of registry, signal, and receiver.

    - `_get_model_classes(app_model)`: Get a list of model classes based on the "app.model" notation.

    - `_get_exclude_models(exclude_tracking_models)`: Get a list of models to exclude from tracking based on settings.

    - `_register_models(models)`: Register models based on the provided list of models or settings.

    - `register_from_settings()`: Register models based on the settings specified in the Django project's settings file. This function checks and validates settings such as inclusion/exclusion of models and fields.

  - **Usage**: The `AuditlogModelRegistry` class is used to register models with auditlog and configure their tracking options. It allows developers to fine-tune which models and fields should be audited for changes. The `register_from_settings` method simplifies the process of registering models based on project settings.

Feel free to use this description and the provided methods in your code documentation. If you have any further questions or need additional assistance, please let me know.

## [📄 **signals.py**](/auditlog/signals.py)

- **Django Auditlog Signals**

  - **Description**: This code defines three custom Django signals used in the Django Auditlog package to handle auditing actions before and after log entries are created. These signals provide a way to intercept and customize auditing behavior in Django applications.

  - **Signals**:

    1. `accessed` Signal:
       - **Description**: This signal is sent whenever an instance of a model is accessed in an `AccessLogDetailView`. It allows for custom handling of access events.
       - **Keyword Arguments**:
         - `sender` (class): The model class that's being audited.
         - `instance` (Any): The actual instance that's being audited.
       - **Usage**: You can connect custom signal handlers to this signal to perform actions when an instance is accessed.

    2. `pre_log` Signal:
       - **Description**: This signal is sent before writing an audit log entry. It provides an opportunity to customize the audit log entry before it's saved.
       - **Keyword Arguments**:
         - `sender` (class): The model class that's being audited.
         - `instance` (Any): The actual instance that's being audited.
         - `action` (auditlog.models.LogEntry.Action): The action on the model resulting in an audit log entry.
       - **Usage**: You can connect custom signal handlers to this signal to modify or add information to the audit log entry before it's created. The return values of these handlers are sent to any `post_log` signal receivers.

    3. `post_log` Signal:
       - **Description**: This signal is sent after writing an audit log entry. It can be used for additional actions or notifications after the log entry has been saved.
       - **Keyword Arguments**:
         - `sender` (class): The model class that's being audited.
         - `instance` (Any): The actual instance that's being audited.
         - `action` (auditlog.models.LogEntry.Action): The action on the model resulting in an audit log entry.
         - `error` (Optional[Exception]): The error, if one occurred while saving the audit log entry (None if no error occurred).
         - `pre_log_results` (List[Tuple[method, Any]]): A list of tuples representing the results of `pre_log` signal receivers. Each tuple contains the receiver method and its corresponding response.
       - **Usage**: You can connect custom signal handlers to this signal to perform additional actions or send notifications after an audit log entry has been created.

  - **Examples**:

    - Connect a custom handler to the `accessed` signal to log access events:

      ```python
      from auditlog.signals import accessed

      def log_access(sender, instance, **kwargs):
          # Custom access logging logic here
          pass

      accessed.connect(log_access)
      ```

    - Connect custom handlers to the `pre_log` and `post_log` signals for additional auditing or notifications:

      ```python
      from auditlog.signals import pre_log, post_log

      def custom_pre_log(sender, instance, action, **kwargs):
          # Custom logic to modify the audit log entry before saving
          pass

      def custom_post_log(sender, instance, action, error, pre_log_results, **kwargs):
          # Custom logic after the audit log entry has been saved
          pass

      pre_log.connect(custom_pre_log)
      post_log.connect(custom_post_log)
      ```
  
  - **Usage**: These signals offer extensibility points for customizing the behavior of the Django Auditlog package in your Django application. You can connect your own signal handlers to these signals to perform actions such as custom logging, notifications, or additional data processing during auditing.