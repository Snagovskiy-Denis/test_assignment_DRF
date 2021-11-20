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


class StreetSlugRelatedField(serializers.SlugRelatedField):
    def get_queryset(self):
        '''Filter Street queryset to ensure unique_together constraint'''
        queryset = super().get_queryset()
        # GET method in Functional Test somehow got here
        # because of that added this guard
        # TODO: test this unexpected error
        if hasattr(self.parent, 'initial_data'):
            request_data = self.parent.initial_data
            city_name = request_data.get('city')
            street_name = request_data.get('street')
            return queryset.filter(name=street_name, city__name=city_name)
        return queryset


class ShopSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(
            slug_field='name',
            queryset=City.objects.all(),
    )
    street = StreetSlugRelatedField(
            slug_field='name',
            queryset=Street.objects.all(),
    )

    def validate(self, attrs):
        '''Validate closing and opening time'''
        if attrs.get('closing_time', 0) < attrs.get('opening_time', 1):
            raise ValidationError('Shop cannot have closing time earlier than opening time')
        return super().validate(attrs)

    class Meta:
        model  = Shop
        fields = ('id', 'name', 'city', 'street', 'house_numbers', 
                'opening_time', 'closing_time', 'is_opened')
