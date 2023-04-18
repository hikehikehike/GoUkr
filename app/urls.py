from django.urls import path, include
from rest_framework import routers

from app.views import CityViewSet, CommentCreateView

router = routers.DefaultRouter()
router.register("city", CityViewSet, basename="city")


urlpatterns = [
    path("", include(router.urls)),
    path("city/<str:slug>/", include(router.urls)),
    path("city/<str:slug>/route/", CityViewSet.as_view({"get": "route"}), name="city-route"),
    path("city/<str:slug>/hotels/", CityViewSet.as_view({"get": "hotels"}), name="city-hotels"),
    path("city/<str:slug>/restaurants/", CityViewSet.as_view({"get": "restaurants"}), name="city-restaurants"),
    path('city/<str:city_slug>/create_comments/', CommentCreateView.as_view(), name='create_comment'),

]

app_name = "app"
