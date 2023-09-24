# 📂 **Account App**

```
account
├── 📁 admin/
├── 📁 migrations/
├── 📁 models/
├── 📁 serializers/
├── 📁 tests/
├── 📁 views/
├── 📄 apps.py
├── 📄 authentication.py
├── 📄 translation.py
├── 📄 urls.py
```

## 📁 **Admin folder**

Django's **Admin** 🛠 is a robust and customizable tool that provides an interface for managing your app's content. The "Account" application uses the "admin" folder to oversee user data.

- 📄 [/account/admin/account.py](/account/admin/account.py)
  - `UserCreationForm` & `UserChangeForm`: 🖊 Forms for managing users.
  - `MyUserAdmin`: ⚙️ Admin settings for the MyUser model.
  - `ProfileAdmin`: 🧑🔧 Admin settings for the user profiles.
  - `NotificationsAdmin`: 🛎️ Admin settings for user notifications.

---

## 📁 **Migration folder**

Migrations 🔄 in Django keep track of model changes and help in smoothly transitioning database schemas.

## 📁 **Models folder**

Models 📋 in Django define the structure of a database table.

- 📄 [/account/models/account.py](/account/models/account.py)
  - `MyUser`: 🧑 Custom user model.
  - `Profile`: 📜 Extended user details.
  - `Notifications`: 🔔 User notifications model.

---

## 📁 **Serializers folder**

Serializers 🔄 in Django convert data for web APIs.

- 📄 [/account/serializers/authenticated.py](/account/serializers/authenticated.py)
  - `LoginSerializer`: 🔑 For user login.
  - `ProfileSerializer`: 📜 For user profiles.
  - `ChangePasswordSerializer`: 🔒 For changing passwords.
  - `NotificationsSerializer`: 🔔 For user notifications.

---

## 📁 **Tests folder**

The "tests" folder 🧪 ensures the app's code reliability.

- 📄 Files:
  - [factories.py](/account/tests/factories.py)
  - [test_admin.py](/account/tests/test_admin.py)
  - [tests.py](/account/tests/tests.py)

---

## 📁 **Views folder**

Views 👀 in Django control how data is displayed and processed.

- 📄 [/account/views/authenticated.py](/account/views/authenticated.py)
  - `LoginAgromapView`: 📌 User login endpoint.
  - `UpdateProfileAPIView`: 📝 Update user profile endpoint.
  - `ChangePasswordAPIView`: 🔒 Change password endpoint.
  - `GetProfileAPIView`: 🧑 Fetch user profile endpoint.
  - `NotificationsAPIView`: 🔔 Get notifications endpoint.
  - `ReadNotificationAPIView`: ✅ Mark notification as read endpoint.
  - `LogoutAgromapView`: 🚪 User logout endpoint.

---

## 📄 **apps.py**

- 📄 [/account/apps.py](/account/apps.py)

It's where the app's configurations 🛠️ are stored.

---

## 📄 **authentication.py**

[Focused on authentication and user activity 🕵️‍♂️.](/account/authentication.py)

- 📄 [/account/authentication.py](/account/authentication.py)
  - `MyTokenAuthentication`: 🔑 Custom token authentication.
  - `AdminLastVisitMiddleware`: ⌚ Tracks user's last activity.
  - `set_cid`: 🔗 Set a correlation ID.
  - `MyAuditMiddleware`: 📝 Extended audit logging.

---

## 📄 **translation.py**

[Translate models 🌐.](/account/translation.py)

---

## 📄 **urls.py**

[It's where the url's configurations 🛠️ are stored.](/account/urls.py)
