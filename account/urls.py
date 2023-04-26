from django.urls import path
from account.views.authenticated import LoginAgromapView, UpdateProfileAPIView, ChangePasswordAPIView, \
    GetProfileAPIView, NotificationsAPIView, DeleteNotificationAPIView, LogoutAgromapView


urlpatterns = [
    path('login_agromap/', LoginAgromapView.as_view()),
    path('logout_agromap/', LogoutAgromapView.as_view()),
    path('edit_profile/', UpdateProfileAPIView.as_view()),
    path('change_password/', ChangePasswordAPIView.as_view()),
    path('get_profile/', GetProfileAPIView.as_view()),
    path('notifications/', NotificationsAPIView.as_view()),
    path('delete_notifications/<int:pk>/',DeleteNotificationAPIView.as_view()),
]