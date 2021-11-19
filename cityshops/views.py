from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status, generics

from cityshops.models import City, Shop, Street
from cityshops.serializers import CitySerializer, ShopSerializer, StreetSerializer


@api_view(['GET'])
def api_root(request):
    '''Api endpoint'''
    table_of_contents = {
        'city': reverse('city-list', request=request),
        'shop': reverse('shop-list', request=request),
    }
    return Response(table_of_contents)


class CityList(generics.ListCreateAPIView):
    '''List all cities or create new city'''

    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityStreetsList(generics.ListCreateAPIView):
    '''List all streets of given city'''

    serializer_class = StreetSerializer

    def get_queryset(self):
        city_pk = self.kwargs.get('city_pk', 0)

        if not City.objects.filter(id=city_pk):
            raise Http404
        return Street.objects.filter(city=city_pk)


class ShopList(APIView):
    '''List all shops or search specific shop or create new shop'''

    serializer_class = ShopSerializer

    def get(self, request, format=None):
        shops = Shop.objects.all()

        if not (filter_params := request.GET):
            serializer = self.serializer_class(shops, many=True)
            return Response(serializer.data)

        for param in filter_params.keys():
            if param not in ('city', 'street', 'opened'): raise Http404

        if (city_name := filter_params.get('city')):
            city = generics.get_object_or_404(City.objects.all(),
                                              name=city_name)
            shops = shops.filter(city=city)

        if (street_name := filter_params.get('street')):
            streets = Street.objects.filter(name=street_name)
            if not streets: raise Http404
            shops = shops.filter(street__in=streets)

        if (opened := filter_params.get('opened')):
            opened = int(opened)
            if opened == 1:
                shops = [shop for shop in shops if shop.is_opened()]
            elif opened == 0:
                shops = [shop for shop in shops if shop.is_closed()]
            else:
                raise Http404

        serializer = self.serializer_class(shops, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        pass
