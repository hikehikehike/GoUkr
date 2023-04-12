from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from app.models import City
from app.parse import parse_hotels
from app.serializers import CityListSerializer, CitySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CityListSerializer
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return CityListSerializer
        if self.action == "route":
            return CitySerializer
        return CitySerializer

    @action(detail=True, url_path="route")
    def route(self, request, slug=None):
        city = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(city)
        return Response(serializer.data)

    @action(detail=True, url_path="hotels")
    def hotels(self, request, slug=None):
        city = self.get_object()
        hotels = parse_hotels(city)

        return Response({"hotels": hotels})
