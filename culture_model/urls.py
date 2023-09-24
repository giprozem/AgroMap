from django.urls import path
from culture_model.views.veg_indexes import VegIndexAPIView

# Define the URL patterns for the culture_model app
urlpatterns = [
    # Map the 'index-list/' URL path to the VegIndexAPIView view
    path('index-list/', VegIndexAPIView.as_view(), name='index-list'),
]
