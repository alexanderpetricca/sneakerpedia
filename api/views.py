from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from sneakers.models import Brand, Sneaker
from api.serializers import BrandSerializer, SneakerSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all().order_by('name')
    serializer_class = BrandSerializer
    http_method_names = ['get', 'head']


    @action(detail=True, methods=['get'])
    def sneakers(self, request, pk=None):
        """
        Returns all Sneakers associated with specified Brand.
        """

        brand = self.get_object()
        sneakers = Sneaker.objects.filter(brand=brand)
        serializer = SneakerSerializer(sneakers, many=True, context={'request': request})
        return Response(serializer.data)    


class SneakerViewSet(viewsets.ModelViewSet):
    queryset = Sneaker.objects.all().order_by('name')
    serializer_class = SneakerSerializer
    http_method_names = ['get', 'head']