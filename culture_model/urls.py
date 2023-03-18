from django.urls import path
from culture_model.views.veg_indexes import VegIndexAPIView


urlpatterns = [
    path('index-list/', VegIndexAPIView.as_view()),
]
