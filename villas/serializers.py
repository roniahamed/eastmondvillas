from rest_framework import serializers
from .models import Property, Media, Booking
from accounts.models import User


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'media_type', 'category', 'file', 'file_url', 'caption', 'is_primary', 'order']
        read_only_fields = ['media_type', 'file_url']



class PropertySerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)
    created_by = serializers.CharField(source='created_by.name', read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'slug', 'description', 'price', 'booking_rate',
            'listing_type', 'status', 'address', 'city', 'max_guests',
            'bedrooms', 'bathrooms', 'has_pool', 'amenities', 'latitude',
            'longitude', 'place_id', 'seo_title', 'seo_description',
            'signature_distinctions', 'staff', 'calendar_link',
            'created_at', 'updated_at', 'assigned_agent', 'created_by',
            'created_by_name',
            'media'
        ]
        read_only_fields = ['slug', 'created_by', 'created_by_name', 'media']

        







        
