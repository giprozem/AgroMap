### Account App

```text
|── account
|   |── admin/
    |── migrations/
|   |── models/
|   |── serializers/
|   |── tests/
|   |── views/
|   |── apps.py
|   |── authentication.py
|   |── translation.py
|   |── urls.py
```

#### Admin folder

The Django Admin is a powerful and customizable tool that provides a user-friendly interface for managing the content of your application without requiring any additional development. By registering your models in admin.py, you can add, edit, delete, and view records in your database directly from this interface. The Django Admin can also be extended and customized to cater to specific administrative needs of the project.

In the context of the "Account" application, the "admin" folder is used to administer user data.

* [/account/admin/account.py](/account/admin/account.py)

***
1

* [*UserCreationForm and UserChangeForm*]: These are forms for creating a new user and changing an existing user, respectively. UserCreationForm requires entering a password and confirming it when creating a user, while UserChangeForm provides the option to change a user's password and displays a link to change the password.

***
2

* [*MyUserAdmin*]: This class provides admin settings for the MyUser model, which represents users in the system. It defines how to display users in the admin list and which fields to show and edit when editing or adding a user. It also specifies read-only fields, such as last_login and date_joined, and defines which fields are available when creating a user through add_fieldsets.

***
3

* [*ProfileAdmin*]: This class registers the Profile model in the Django admin panel. It defines how to display user profiles, including their full names, and allows searching by full name or username.

***
4

* [*NotificationsAdmin*]: This class registers the Notifications model in  the admin panel. It uses TranslationAdmin, which may indicate that the model supports translations. It displays information about notifications, including the associated user, and allows filtering notifications by user.

***

#### Migration folder

Migrations in Django are designed to be a lightweight, consistent way to make database schema changes without having to manually write SQL code. The migrations system keeps track of changes to models and provides a mechanism to apply or reverse these changes in a structured manner. This allows developers to evolve their database schema over time, ensuring that the application and database remain in sync. Migrations are generated automatically when you run the makemigrations command and can be applied to the database using the migrate command.

#### Models folder

In Django, models are Python classes that define the structure of a database table, representing and interacting with the data stored in it using the Object-Relational Mapping (ORM) system. They allow developers to manage and query data in a high-level, Pythonic way without writing raw SQL.

* [/account/models/account.py](/account/models/account.py)

***
1

* [*MyUser*]: This is a custom user model that handles user authentication and management in the Django project. It extends the built-in AbstractUser class to add specific fields that determine the user's type, such as is_staff, is_farmer, is_employee, and is_supervisor. It also chooses not to utilize the default first_name and last_name fields from the parent class by setting them to None. When an instance of this model is represented as a string, it returns the username.

***

2

* [*Profile*]: This model is meant to store additional details about a user, like their full name and phone number. There's a one-to-one relationship between the Profile and MyUser models, ensuring that each user can have only one associated profile. When an instance of this model is represented as a string, it returns the username of the linked user.

***
3

* [*Notifications*]: This model is designed to handle user notifications. It allows associating a notification with a specific user and tracks whether the notification has been read or not. The model contains fields for the user (with a foreign key relationship to the MyUser model), the date of notification creation, the text of the notification, and a Boolean field to check if the notification has been read. When represented as a string, an instance of this model returns the notification text.

#### Serializers folder

Serializers in Django convert complex data, like database records, into JSON for web APIs and enable the reverse process. They are crucial for handling data communication between a Django app and clients or services.

* [/account/serializers/authetificated.py](/account/serializers/authetificated.py)

***
1

* [*LoginSerializer*]: This serializer is used for user login purposes.
        It uses basic fields, i.e., username and password.
        It doesn't connect to any model, and instead, defines the fields directly.

***
2

* [*ProfileSerializer*]: This serializer is related to the user profile.
        It's based on the Profile model.
        The fields it exposes for serialization are full_name and phone_number.

***
3

* [*ChangePasswordSerializer*]: This serializer is designed for changing a user's password.
        It contains three fields: old_password, password, and password_confirm.
        The validate method is overridden to check the validity of the input:
            It ensures the old_password matches the current user's password.
            It also checks to ensure that the new password and password_confirm fields match each other.
        If any of these checks fail, it raises a ValidationError with an appropriate message.

***
4

* [*NotificationsSerializer*]: This serializer relates to user notifications.
        It's based on the Notifications model.
        It serializes all fields from the model except for the text field, which is explicitly excluded.

#### Tests folder

The "tests" folder in a Django application is used for writing and organizing unit tests and test cases to ensure the correctness and reliability of the application's code. These tests help developers catch and fix errors, verify that new code changes don't break existing functionality, and maintain the overall quality of the application's codebase.

* [/account/tests/factories.py](/account/tests/factories.py)
* [/account/tests/test_admin.py](/account/tests/test_admin.py)
* [/account/tests/tests.py](/account/tests/tests.py)

#### Views folder

In a Django application, "views" are Python functions or classes responsible for processing HTTP requests and returning appropriate HTTP responses. They define the logic for handling user requests, interacting with models and templates, and generating dynamic content to be displayed in a web application. Views play a crucial role in controlling what data is displayed to users and how user interactions are processed within the application.

* [/account/views/authenticated.py](/account/views/authenticated.py)

***
1

* [*LoginAgromapView*]:
        This endpoint allows users to log in.
        It uses the LoginSerializer to validate the incoming data.
        If the credentials are valid, it authenticates the user and returns an authentication token, user ID, username, superuser status, and active status.
        swagger_auto_schema is used to generate OpenAPI documentation for this endpoint.

***
2

* [*UpdateProfileAPIView*]:
        This endpoint enables authenticated users to update their profiles.
        It fetches the profile linked to the authenticated user, then updates it based on the received data.

***
3

* [*ChangePasswordAPIView*]:
        Allows authenticated users to change their password.
        The new password is set after validating that the old password is correct and that the new password and its confirmation match.

***
4

* [*GetProfileAPIView*]:
        Fetches and returns the profile of the authenticated user.

***
5

* [*NotificationsAPIView*]:
        Returns a list of unread notifications for the authenticated user.

***
6

* [*ReadNotificationAPIView*]:
        Enables the user to mark a specific notification as read.
        If the specified notification isn't found, it returns a message indicating that the token wasn't found (note: the message might be misleading as it's not a token that's being searched for but rather a notification).

***
7

* [*LogoutAgromapView*]:
        Deletes the authenticated user's token, effectively logging them out.

#### apps.py

* [/account/apps.py](/account/apps.py)

The "apps.py" file in a Django application is used to configure and customize the behavior of the application itself. It allows developers to define various application-specific settings and configurations, including specifying application metadata, registering application-specific signals, and performing other initialization tasks. This file serves as a central place for managing application-level configurations and behaviors in a Django project.

#### authentication.py

This module provides several enhancements and customizations over the default Django and Django Rest Framework (DRF) behaviors, specifically focused on authentication, user activity tracking, and audit logging.

* [/account/authentication.py](/account/authentication.py)

***
1

* [*MyTokenAuthentication*]:
        A custom token authentication class that extends the default TokenAuthentication from DRF.
        It authenticates users based on tokens and also updates the last login timestamp for the user whenever their token is used for authentication.

***
2

* [*AdminLastVisitMiddleware*]:
        A middleware that updates the last login timestamp for any authenticated user every time they make a request.
        This ensures that the system keeps track of the user's latest activity.

***
3

* [*set_cid*]:
        A function designed to set a correlation ID from the request headers into a context variable.
        Correlation IDs are often used in distributed systems to trace requests across multiple services. In the context of audit logging, this might be useful to correlate audit logs with other logs or systems.

***
4

* [*MyAuditMiddleware*]:
        An extension of the AuditlogMiddleware which is probably from the django-auditlog library.
        It determines the actor (i.e., the user) from the token present in the request headers.
        It sets both the actor and the remote address (probably the IP address) for the purposes of audit logging.
        Additionally, it sets the correlation ID for the request using the set_cid function.
