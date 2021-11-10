from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status, generics

from cityshops.models import City, Street
from cityshops.serializers import CitySerializer, StreetSerializer


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

    def get(self, request, city_pk, format=None):
        '''Returns list of city streets

        If city does not exist then return status 404
        '''

        if not City.objects.filter(id=city_pk):
            raise Http404
        streets = Street.objects.filter(city=city_pk)
        serializer = self.serializer_class(streets, many=True)
        return Response(serializer.data)
