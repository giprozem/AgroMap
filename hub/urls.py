from django.urls import path

from hub.views.zem_balance_api import AsrEniCodeAPIView

urlpatterns = [
    path('get-eni-code/', AsrEniCodeAPIView.as_view()),

]