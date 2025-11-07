from rest_framework import serializers
from .models import Villa, VillaImage, Amenity, Booking


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ('id', 'name')


class VillaImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    # expose computed/public URL of the stored image
    image_url = serializers.ReadOnlyField(source='image_url')

    class Meta:
        model = VillaImage
        fields = ('id', 'image', 'image_url', 'caption', 'type', 'is_primary', 'order')

    def validate(self, attrs):
        # On create, require an uploaded image
        if not self.instance and not attrs.get('image'):
            raise serializers.ValidationError('An image file is required.')
        return attrs


class VillaSerializer(serializers.ModelSerializer):
    images = VillaImageSerializer(many=True, read_only=True)
    # allow frontend to send a list of amenity ids when creating/updating
    amenities = serializers.PrimaryKeyRelatedField(queryset=Amenity.objects.all(), many=True, required=False)
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Villa
        fields = ('id', 'owner', 'slug', 'title', 'description', 'price', 'property_type', 'max_guests', 'address', 'city', 'bedrooms', 'bathrooms', 'has_pool', 'amenities', 'latitude', 'longitude', 'place_id', 'seo_title', 'seo_description', 'signature_distinctions', 'staff', 'calendar_link', 'status', 'images')

    def create(self, validated_data):
        amenities = validated_data.pop('amenities', [])
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data.setdefault('owner', request.user)
        villa = Villa.objects.create(**validated_data)
        if amenities:
            villa.amenities.set(amenities)
        return villa

    def update(self, instance, validated_data):
        amenities = validated_data.pop('amenities', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if amenities is not None:
            instance.amenities.set(amenities)
        return instance


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Booking
        fields = ('id', 'villa', 'user', 'full_name', 'email', 'phone', 'check_in', 'check_out', 'status', 'total_price', 'google_event_id', 'created_at')

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)
