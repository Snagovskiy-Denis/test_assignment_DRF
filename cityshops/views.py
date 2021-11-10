from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status, generics

from cityshops.models import City
from cityshops.serializers import CitySerializer


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


class CityStreetsList(APIView):
    '''List all streets of given city'''
