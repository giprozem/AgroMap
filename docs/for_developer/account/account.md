# 📂 **Account App**

```
account
├── 📁 admin/
    ├── 📄 account.py

├── 📁 migrations/
├── 📁 models/
    ├── 📄 account.py

├── 📁 serializers/
    ├── 📄 authentication.py

├── 📁 tests/
    ├── 📄 factories.py
    ├── 📄 test_admin.py
    ├── 📄 tests.py

├── 📁 views/
    ├── 📄 authentication.py

├── 📄 apps.py
├── 📄 authentication.py
├── 📄 translation.py
├── 📄 urls.py
```

## 📁 **Admin folder**

Django's **Admin** 🛠 is a robust and customizable tool that provides an interface for managing your app's content. The "Account" application uses the "admin" folder to oversee user data.

## User Management in Django Admin

### UserCreationForm

- **Purpose**: This form is used to create a new user through the Django admin panel. It includes fields for a password and its confirmation.
- **Fields**:
  - `password`: A required field for the user's password.
  - `confirm_password`: A required field for confirming the password.
- **Validation**: It ensures that the password and its confirmation match.
- **Usage**: It is used for adding new users via the Django admin panel.

### UserChangeForm

- **Purpose**: This form is used to update existing user records through the Django admin panel. It displays information about the user's password but does not allow changes to it.
- **Fields**:
  - `password`: Displays the user's password (read-only) and provides a link to change it.
- **Usage**: It is used for updating user records via the Django admin panel.

### MyUserAdmin (User Administration)

- **Purpose**: The `MyUserAdmin` class provides administrative options for the `MyUser` model (custom user model).
- **Forms**: 
  - `form`: Uses `UserChangeForm` for changing user records.
  - `add_form`: Uses `UserCreationForm` for adding new users.
- **List Display**: Displays the user's last login timestamp and username.
- **Read-only Fields**: Shows the last login and date joined fields as read-only.
- **Fieldsets**:
  - `None`: Includes fields for `username` and `password`.
  - `Permissions`: Includes fields for managing user permissions and group memberships.
- **Add Fieldsets**: Defines the layout for adding new users, including fields for `username`, `password`, permissions, and group memberships.
- **Usage**: It provides user management capabilities in the Django admin panel, allowing administrators to add and update user records.

### ProfileAdmin

- **Purpose**: The `ProfileAdmin` class is used to manage user profiles in the Django admin panel.
- **List Display**: Displays the associated user (`my_user`) and the user's full name.
- **Search Fields**: Allows searching for profiles based on the full name or the associated user's username.
- **Usage**: It provides a user-friendly interface for managing user profiles.

### NotificationsAdmin

- **Purpose**: The `NotificationsAdmin` class is used to manage user notifications in the Django admin panel.
- **List Display**: Displays the associated user and its notifications.
- **List Filter**: Allows filtering notifications by user.
- **Usage**: It provides an interface for administrators to manage user notifications.

These admin configurations enhance user management and profile management within the Django admin panel. They facilitate the creation, updating, and management of user records, profiles, and notifications.


## 📁 **Migration folder**

Migrations 🔄 in Django keep track of model changes and help in smoothly transitioning database schemas.

## 📁 **Models folder**

## User Management Models in Django

### MyUser Model

- **Purpose**: The `MyUser` model is a custom user model designed for user authentication and management in a Django project. It extends the built-in `AbstractUser` class to include additional fields that indicate the type of user, such as administrators, farmers, workers, and observers.
- **Fields**:
  - `is_staff`: A boolean field indicating whether the user is an administrator.
  - `is_farmer`: A boolean field indicating whether the user is a farmer.
  - `is_employee`: A boolean field indicating whether the user is a worker.
  - `is_supervisor`: A boolean field indicating whether the user is an observer.
  - `username`: The unique username used for authentication.
- **Usage**: This model allows the system to distinguish between different user roles and permissions.

### Profile Model

- **Purpose**: The `Profile` model stores additional information about users of the application. It is linked to the `MyUser` model using a one-to-one relationship, allowing each user to have a corresponding profile with details such as full name and phone number.
- **Fields**:
  - `my_user`: A one-to-one relationship to the associated `MyUser` instance.
  - `full_name`: A field for the user's full name.
  - `phone_number`: A field for the user's phone number.
- **Usage**: This model provides a way to store and manage additional user information beyond authentication data.

### Notifications Model

- **Purpose**: The `Notifications` model stores notifications for users. It allows you to associate notifications with specific users and track whether a notification has been read or not.
- **Fields**:
  - `user`: A foreign key to the associated `MyUser` instance.
  - `date`: A timestamp indicating the creation date of the notification.
  - `text`: A field for the notification text.
  - `is_read`: A boolean field indicating whether the notification has been read.
- **Usage**: This model enables the application to send, store, and track notifications for individual users.

These models provide the foundation for user management, user profiles, and notifications within the Django project. They are designed to support user authentication, store user-specific information, and manage user notifications efficiently.


## 📁 **Serializers folder**

Serializers 🔄 in Django convert data for web APIs.

- 📄 [/account/serializers/authenticated.py](/account/serializers/authetificated.py)

## Serializers for User Management in Django

### LoginSerializer

- **Purpose**: The `LoginSerializer` is used for user login. It defines fields for the username and password, allowing users to authenticate.
- **Fields**:
  - `username`: A field for the username.
  - `password`: A field for the password.
- **Usage**: This serializer is used when users log in to the system.

### ProfileSerializer

- **Purpose**: The `ProfileSerializer` is used for serializing user profile information, including the user's full name and phone number.
- **Fields**:
  - `full_name`: A field for the user's full name.
  - `phone_number`: A field for the user's phone number.
- **Usage**: This serializer is used to provide a representation of the user's profile information.

### ChangePasswordSerializer

- **Purpose**: The `ChangePasswordSerializer` is used for changing a user's password. It includes fields for the old password, new password, and password confirmation.
- **Fields**:
  - `old_password`: A field for the old password.
  - `password`: A field for the new password.
  - `password_confirm`: A field to confirm the new password.
- **Validation**: This serializer validates that the old password is correct and that the new password and confirmation match.
- **Usage**: This serializer is used when a user wants to change their password.

### NotificationsSerializer

- **Purpose**: The `NotificationsSerializer` is used for serializing user notifications. It includes fields for user-specific notification data, excluding the actual notification text.
- **Fields**:
  - Excludes the `text` field, which contains the actual notification text.
- **Usage**: This serializer is used to provide a representation of user notifications, excluding the text content.

These serializers are essential for handling user authentication, profile information, password changes, and notifications in the Django application. They define the structure and behavior for data interchange between the client and server.


## 📁 **Tests folder**

The "tests" folder ensures the app's code reliability.

- 📄 Files:
  - [factories.py](/account/tests/factories.py)
  - [test_admin.py](/account/tests/test_admin.py)
  - [tests.py](/account/tests/tests.py)

---

## 📁 **Views folder**

Views 👀 in Django control how data is displayed and processed.

- 📄 [/account/views/authenticated.py](/account/views/authenticated.py)

## API Views for User Authentication and Management

### LoginAgromapView

- **Purpose**: This API view is used for user login. It authenticates users with their username and password, returning an authentication token upon successful login.
- **HTTP Method**: POST
- **Request Body**:
  - `username` (string): The user's username.
  - `password` (string): The user's password.
- **Responses**:
  - 200 (Success):
    - `token` (string): An authentication token for the user.
    - `user_id` (integer): The user's ID.
    - `username` (string): The user's username.
    - `is_superuser` (boolean): Indicates if the user is a superuser.
    - `is_active` (boolean): Indicates if the user's account is active.

### UpdateProfileAPIView

- **Purpose**: This generic API view is used to update a user's profile information, such as full name and phone number.
- **HTTP Method**: PATCH
- **Permissions**: Requires authentication (IsAuthenticated).
- **Request Body**: Accepts the fields to be updated.
- **Responses**: Returns the updated user profile.

### ChangePasswordAPIView

- **Purpose**: This API view is used for changing a user's password. It requires the user to provide the old password, new password, and password confirmation.
- **HTTP Method**: POST
- **Permissions**: Requires authentication (IsAuthenticated).
- **Request Body**:
  - `old_password` (string): The user's old password.
  - `password` (string): The user's new password.
  - `password_confirm` (string): The confirmation of the new password.
- **Responses**:
  - Success: Returns a message indicating that the password was changed.

### GetProfileAPIView

- **Purpose**: This generic API view is used to retrieve a user's profile information.
- **HTTP Method**: GET
- **Permissions**: Requires authentication (IsAuthenticated).
- **Responses**: Returns the user's profile information.

### NotificationsAPIView

- **Purpose**: This List API view is used to retrieve a list of unread notifications for the authenticated user.
- **HTTP Method**: GET
- **Permissions**: Requires authentication (IsAuthenticated).
- **Responses**: Returns a list of unread notifications.

### ReadNotificationAPIView

- **Purpose**: This generic API view is used to mark a notification as read.
- **HTTP Method**: PATCH
- **Permissions**: Requires authentication (IsAuthenticated).
- **URL Parameter**:
  - `pk` (integer): The ID of the notification to mark as read.
- **Responses**:
  - Success: Returns a message indicating that the notification was marked as read.

### LogoutAgromapView

- **Purpose**: This API view is used for user logout. It deletes the user's authentication token upon logout.
- **HTTP Method**: GET
- **Permissions**: Requires authentication (IsAuthenticated).
- **Responses**: Returns a message indicating that the authentication token was deleted.

These API views provide essential functionality for user authentication, profile management, password change, notification handling, and logout in the Django application.


## 📄 **apps.py**

- 📄 [/account/apps.py](/account/apps.py)

It's where the app's configurations 🛠️ are stored.

---

## 📄 **authentication.py**

[Focused on authentication and user activity .](/account/authentication.py)

- 📄 [/account/authentication.py](/account/authentication.py)

## Custom Token Authentication

### MyTokenAuthentication

- **Purpose**: Custom token authentication class that extends TokenAuthentication. It provides enhanced token-based authentication for users.
- **Description**: This authentication class checks the validity of the authentication token and verifies that the associated user is active. It also updates the user's last login timestamp upon successful authentication.

## Middleware for Admin Last Visit Tracking

### AdminLastVisitMiddleware

- **Purpose**: Middleware to track the last visit timestamp of authenticated users, specifically designed for admin users.
- **Description**: This middleware checks if a user is authenticated, and if so, updates their last login timestamp in the database upon each request.

## Middleware for Audit Logging

### MyAuditMiddleware

- **Purpose**: Custom middleware for audit logging that extends AuditlogMiddleware. It is responsible for setting the actor and remote address for audit logs and handling correlation IDs.
- **Description**: This middleware is used to set the actor (user) and remote address for audit logs. It also handles correlation IDs, which can be used for tracing requests. The actor is determined based on the authentication token provided in the request.

## Context Variable Setter

### set_cid

- **Purpose**: Function to set the correlation ID (CID) context variable.
- **Description**: This function sets the correlation ID context variable based on a header in the HTTP request. It can be used to associate requests with specific correlation IDs for tracing purposes.

These custom components enhance authentication, user tracking, and audit logging in the Django application. The `MyTokenAuthentication` class ensures secure user authentication, the `AdminLastVisitMiddleware` tracks admin users' last visits, and the `MyAuditMiddleware` enables comprehensive audit logging with actor and remote address tracking.


## 📄 **translation.py**

[Translate models 🌐.](/account/translation.py)

---

## 📄 **urls.py**

[It's where the url's configurations 🛠️ are stored.](/account/urls.py)
