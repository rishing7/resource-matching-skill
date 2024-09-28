from django.urls import path
from resources.api.resource_views import matched_resources

urlpatterns = [
    path("matched-resources/", matched_resources, name="matched_resources"),
]
