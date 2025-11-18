from rest_framework import serializers
from .models import Property, Media, Booking
from accounts.models import User
from datetime import date



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



class BookingPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'title']


class BookingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']

class BookingSerializer(serializers.ModelSerializer):
    property_details = BookingPropertySerializer(source='property', read_only=True)
    user_details = BookingUserSerializer(source='user', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id','property', 'email','phone','check_in','check_out','total_price','user','status','google_event_id','created_at','property_details','user_details']
        read_only_fields = ['user', 'status', 'google_event_id', 'created_at']
        extra_kwargs = {
            'property': {'write_only': True}
        }

        def validate(self, data):
            if 'check_in' in data and 'check_out' in data:
                if data['check_in'] >= data['check_out']:
                    raise serializers.ValidationError({"check_out": "Check-out date must be after check-in date."})
            
            if 'check_in' in data:
                if data['check_in'] < date.today():
                    raise serializers.ValidationError({"check_in": "Check-in date cannot be in the past."})
            return data






        
