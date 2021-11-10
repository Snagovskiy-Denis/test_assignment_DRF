from django.core.exceptions import ValidationError
from rest_framework import serializers

from cityshops.models import City, Shop, Street


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model  = City
        fields = ('id', 'name')


class StreetSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Street
        fields = ('id', 'name', 'city')
        extra_kwargs = {
            'city': {'write_only': True},  # exclude city_id from print
        }


class ShopSerializer(serializers.ModelSerializer):
    city_name = serializers.ReadOnlyField(source='city.name')
    street_name = serializers.ReadOnlyField(source='street.name')

    def validate(self, attrs):
        '''Validate closing and opening time'''
        if attrs.get('closing_time', 0) < attrs.get('opening_time', 1):
            raise ValidationError('Shop cannot have closing time earlier than opening time')
        return super().validate(attrs)

    class Meta:
        model  = Shop
        fields = ('id', 'name', 'city_name', 'street_name', 'house_numbers', 
                'opening_time', 'closing_time', 'is_opened')
