from rest_framework import serializers

from cityshops.models import City


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model  = City
        fields = ('id', 'name')
