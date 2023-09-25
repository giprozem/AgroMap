# 📂 **Config**

-----
```
📁 **config**
│
├── 📄 asgi.py
├── 📄 settings.py
├── 📄 urls.py
└── 📄 wsgi.py

```

These directories are important components of the Django application structure and help manage settings, database, and other aspects of your web project.

## [📄 **asgi.py**](/config/asgi.py)

- **Django ASGI (asgi.py) Script**

  - **Description**: The `asgi.py` script is a Python script used in Django web applications to provide an entry point for handling asynchronous web requests using the ASGI (Asynchronous Server Gateway Interface) specification. ASGI allows Django to handle asynchronous operations, such as WebSockets, long-polling, and other real-time functionality, in addition to traditional synchronous HTTP requests.

  - **Import Statements**:
    - `os`: The `os` module is imported to work with operating system-related functionality.
    - `django.core.asgi.get_asgi_application`: The `get_asgi_application` function from Django's ASGI module is imported. It's used to retrieve the ASGI application for the Django project.

  - **Environment Configuration**:
    - `os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")`: This line sets the default Django settings module for the application. It specifies the Python path to the settings module, allowing Django to configure the application based on the specified settings.

  - **ASGI Application Initialization**:
    - `application = get_asgi_application()`: This line initializes the ASGI application by calling the `get_asgi_application` function. It retrieves the ASGI application instance based on the project's settings.

  - **Usage**:
    - The `asgi.py` script serves as the entry point for handling asynchronous requests in a Django application. It's essential when enabling real-time functionality, such as WebSockets or handling long-polling requests.
    - ASGI support in Django enables the application to handle both traditional synchronous HTTP requests and asynchronous operations, making it suitable for modern, interactive web applications.

  - **Note**:
    - ASGI is particularly useful for applications that require real-time features, as it allows Django to work seamlessly with asynchronous frameworks and protocols.

- **Example**:
  - Here's an example of a simple `asgi.py` script in a Django project:

    ```python
    import os
    from django.core.asgi import get_asgi_application

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    application = get_asgi_application()
    ```

  - This script sets up the ASGI application for the Django project, making it ready to handle both synchronous and asynchronous requests.

- **References**:
  - [ASGI (Asynchronous Server Gateway Interface) Specification](https://asgi.readthedocs.io/en/latest/)
  - [Django ASGI Support](https://docs.djangoproject.com/en/3.2/howto/asynchronous/)

## [📄 **settings.py**](/config/settings.py)

- **Django Settings Configuration (settings.py)**

  - **Description**: The `settings.py` file is an essential part of a Django application, responsible for configuring various settings and parameters for the application's operation. This file contains a wide range of configurations, including database settings, middleware, internationalization, and more.

  - **Base Directory Configuration**:
    - `BASE_DIR`: Defines the base directory of the Django project using Python's `Path` module. It helps in specifying the project's directory structure.

  - **Secret Key Configuration**:
    - `SECRET_KEY`: Specifies the secret key used for securing the Django application. It is typically stored in environment variables for security.

  - **Debug Mode**:
    - `DEBUG`: Determines whether the application is in debug mode. Set to `True` for development and should be `False` in production.

  - **Allowed Hosts**:
    - `ALLOWED_HOSTS`: Specifies the allowed hosts for the application. Requests from hosts not in this list will be denied.

  - **CSRF Protection Configuration**:
    - `CSRF_TRUSTED_ORIGINS`: Defines trusted origins for Cross-Site Request Forgery (CSRF) protection. Requests from trusted origins are exempt from CSRF checks.

  - **Installed Applications**:
    - `INSTALLED_APPS`: Lists the Django applications and additional libraries installed in the project. Applications provide specific functionality, while libraries are external packages integrated into the project.

  - **Middleware Configuration**:
    - `MIDDLEWARE`: Specifies a list of middleware classes that process requests and responses. Middleware can perform tasks like security checks, handling sessions, and more.

  - **Root URL Configuration**:
    - `ROOT_URLCONF`: Points to the URL configuration module for the project, which defines the routing of URLs to views.

  - **Template Settings**:
    - `TEMPLATES`: Configures the template engine and its options, including template directories and context processors.

  - **WSGI Application Entry Point**:
    - `WSGI_APPLICATION`: Defines the entry point for the WSGI (Web Server Gateway Interface) application, responsible for serving the application over HTTP.

  - **Database Configuration**:
    - `DATABASES`: Configures the database connection, specifying the database engine, name, user, password, host, and port.

  - **Password Validation Settings**:
    - `AUTH_PASSWORD_VALIDATORS`: Defines a list of password validation checks to ensure strong and secure user passwords.

  - **Language and Timezone Settings**:
    - `LANGUAGE_CODE`: Specifies the default language for the application.
    - `TIME_ZONE`: Sets the default timezone for the application's date and time operations.

  - **Locale and Translation**:
    - `LOCALE_PATHS` and `LANGUAGES`: Configure localization and translation settings to support multiple languages.

  - **Custom User Model**:
    - `AUTH_USER_MODEL`: Defines a custom user model for the application, allowing customization of the user authentication system.

  - **Static and Media Files Settings**:
    - `STATIC_URL` and `STATIC_ROOT`: Specify the URL and root directory for serving static files.
    - `MEDIA_URL` and `MEDIA_ROOT`: Define the URL and root directory for handling media files (user uploads).

  - **CORS (Cross-Origin Resource Sharing) Settings**:
    - `CORS_ALLOW_ALL_ORIGINS`: Allows all origins to make cross-origin requests to the application.

  - **Leaflet Map Configuration**:
    - `LEAFLET_CONFIG`: Configures the Leaflet map with default settings.

  - **REST Framework Settings**:
    - `REST_FRAMEWORK`: Configures settings for the Django REST framework, including authentication and filtering options.

  - **Jazzmin Settings**:
    - `JAZZMIN_SETTINGS` and `JAZZMIN_UI_TWEAKS`: Define settings for the Jazzmin admin panel, including its appearance and customization options.

  - **Apache Kafka Configuration**:
    - `KAFKA_HOST_PORT`: Specifies the hostname and port for connecting to an Apache Kafka server.

  - **Usage**:
    - The `settings.py` file is a central configuration file for Django projects. It allows developers to customize the behavior of the application, including database connections, security settings, internationalization, and more.
  
  - **Note**:
    - Sensitive information such as `SECRET_KEY` and database credentials should be stored securely and not hard-coded in the file. Environment variables or dedicated configuration files are recommended for such sensitive data.

- **Example**:
  - The provided `settings.py` file is an example configuration for a Django application. It demonstrates various settings and configurations commonly used in Django projects.

- **References**:
  - [Django Settings Documentation](https://docs.djangoproject.com/en/3.2/ref/settings/)
  - [Django REST Framework Documentation](https://www.django-rest-framework.org/)
  - [Jazzmin - Django Admin Panel Customization](https://wsvincent.com/django-jazzmin/)

## [📄 **urls.py**](/config/urls.py)

- **Django URL Configuration (urls.py)**

  - **Description**: The `urls.py` file is used to define the URL patterns for routing incoming HTTP requests to view functions in a Django application. It also includes configurations for internationalization, API documentation, and serving media and static files during development.

  - **URL Patterns**:
    - `path("i18n/", include("django.conf.urls.i18n"))`: Includes URL patterns for internationalization and language switching.
    - `path('hub/', include("hub.urls"))`: Routes requests with the path prefix "hub/" to the "hub" application's URLs.
    - `path('veg/', include('indexes.urls'))`: Routes requests with the path prefix "veg/" to the "indexes" application's URLs.
    - `path('gip/', include('gip.urls'))`: Routes requests with the path prefix "gip/" to the "gip" application's URLs.
    - `path('docs/', schema_view.with_ui())`: Provides API documentation using `drf_yasg` with a user interface.
    - `path("schema/", Schema.as_view())`: Handles requests for generating and viewing the database schema graph.
    - `path('info/', include('culture_model.urls'))`: Routes requests with the path prefix "info/" to the "culture_model" application's URLs.
    - `path('ai/', include('ai.urls'))`: Routes requests with the path prefix "ai/" to the "ai" application's URLs.
    - `path('account/', include('account.urls'))`: Routes requests with the path prefix "account/" to the "account" application's URLs.

  - **Internationalization Patterns**:
    - `i18n_patterns`: Wraps the admin URLs with internationalization patterns for language selection.

  - **Serving Media and Static Files**:
    - If `DEBUG` is `True` (indicating a development environment), the application serves media and static files:
      - `urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`: Serves media files (e.g., user uploads).
      - `urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)`: Serves static files (e.g., CSS, JavaScript) from the specified root directory.

  - **Admin Site Customization**:
    - `admin.site.site_header`: Customizes the header text of the Django admin site.
    - `admin.site.index_title`: Sets the title for the admin index page.

  - **API Documentation (Swagger)**:
    - Utilizes `drf_yasg` to create an OpenAPI schema view for API documentation with a title and default version.

- **References**:
  - [Django URL dispatcher](https://docs.djangoproject.com/en/3.2/topics/http/urls/)
  - [drf-yasg Documentation](https://drf-yasg.readthedocs.io/en/stable/)
  - [Schema Graph for Django](https://pypi.org/project/django-schema-graph/)
  
This description provides an overview of the key URL patterns and configurations found in the `urls.py` file of a Django application. It defines how incoming requests are mapped to specific views and includes settings for internationalization, API documentation, and serving files.

## [📄 **wsgi.py**](/config/wsgi.py)

- **Django WSGI Configuration (wsgi.py)**

  - **Description**: The `wsgi.py` file is used to configure and initialize the WSGI application for serving a Django web application using WSGI-compliant web servers such as Apache, Nginx, or Gunicorn.

  - **Import Statements**:
    - `import os`: Importing the `os` module for working with environment variables.
    - `from django.core.wsgi import get_wsgi_application`: Importing the `get_wsgi_application` function from Django's WSGI module.

  - **Environment Configuration**:
    - `os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")`: Setting the default Django settings module to `"config.settings"` using the `os.environ.setdefault` method. This ensures that Django uses the specified settings module when initializing the application.

  - **WSGI Application Initialization**:
    - `application = get_wsgi_application()`: Initializing the WSGI application using the `get_wsgi_application` function from Django's WSGI module. This line creates the WSGI application instance that will handle incoming HTTP requests and route them to the appropriate views and handlers defined in the Django application.

  - **References**:
    - [Django WSGI Configuration](https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/)
    - [WSGI (Web Server Gateway Interface)](https://wsgi.readthedocs.io/en/latest/)

This description provides an overview of the key components and configurations found in the `wsgi.py` file of a Django application. It specifies the default Django settings module, initializes the WSGI application, and prepares the application for deployment on WSGI-compliant web servers.
