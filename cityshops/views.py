from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.serializers import ValidationError

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
            raise ValidationError({'city': 'no such city in database'})
        return Street.objects.filter(city=city_pk)


class ShopList(generics.ListCreateAPIView):
    '''List all shops or search specific shop or create new shop'''

    valid_search_parameters = ('city', 'street', 'opened')
    serializer_class = ShopSerializer

    def validate_search_parameters(self, search_parameters: dict):
        for parameter in search_parameters:
            if parameter not in self.valid_search_parameters:
                msg = 'Got invalid search parameter = "{}"'
                raise ValidationError(msg.format(parameter))

        if opened := search_parameters.get('opened'):
            if not opened.isnumeric() or int(opened) not in (0, 1):
                msg = 'must be 0 or 1, not "{}"'
                raise ValidationError({'opened': msg.format(opened)})

    def get_queryset(self):
        queryset = Shop.objects.all()

        if not (search_parameters := self.request.query_params):
            return queryset

        self.validate_search_parameters(search_parameters)

        if city_name := search_parameters.get('city'):
            queryset = queryset.filter(city__name=city_name)

        if street_name := search_parameters.get('street'):
            queryset = queryset.filter(street__name=street_name)

        if opened := search_parameters.get('opened'):
            check_open = bool(int(opened))
            check_function = Shop.is_opened if check_open else Shop.is_closed
            queryset = [shop for shop in queryset if check_function(shop)]

        return queryset
