from django.urls import path, include
from rest_framework import routers

from app.views import CityViewSet

router = routers.DefaultRouter()
router.register("city", CityViewSet, basename="city")


urlpatterns = [
    path("", include(router.urls)),
    path("cities/<str:slug>/", include(router.urls)),
    path("cities/<str:slug>/route/", CityViewSet.as_view({"get": "route"}), name="city-route"),
    path("cities/<str:slug>/hotels/", CityViewSet.as_view({"get": "hotels"}), name="city-hotels"),
    path("cities/<str:slug>/restaurants/", CityViewSet.as_view({"get": "restaurants"}), name="city-restaurants"),
]

app_name = "app"
