from django.urls import path
from account.views.authenticated import (
    LoginAgromapView,
    UpdateProfileAPIView,
    ChangePasswordAPIView,
    GetProfileAPIView,
    NotificationsAPIView,
    LogoutAgromapView,
    ReadNotificationAPIView,
)

urlpatterns = [
    # URL pattern for user login.
    path('login_agromap/', LoginAgromapView.as_view()),

    # URL pattern for user logout.
    path('logout_agromap/', LogoutAgromapView.as_view()),

    # URL pattern for updating user profile information.
    path('edit_profile/', UpdateProfileAPIView.as_view()),

    # URL pattern for changing user password.
    path('change_password/', ChangePasswordAPIView.as_view()),

    # URL pattern for retrieving user profile information.
    path('get_profile/', GetProfileAPIView.as_view()),

    # URL pattern for retrieving user notifications.
    path('notifications/', NotificationsAPIView.as_view()),

    # URL pattern for marking a notification as read.
    path('notifications/<int:pk>/', ReadNotificationAPIView.as_view()),
]