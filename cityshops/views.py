from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status

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


class CityList(APIView):
    '''List all cities or create new city'''

    def get(self, request, format=None):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
