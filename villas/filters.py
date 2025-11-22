from django_filters import rest_framework as filters
from .models import Property
from datetime import date

class PropertyFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    min_beds = filters.NumberFilter(field_name="bedrooms", lookup_expr='gte')
    min_baths = filters.NumberFilter(field_name="bathrooms", lookup_expr='gte')

    guests = filters.NumberFilter(field_name="add_guest", lookup_expr='gte')

    class Meta:
        model = Property
        fields = ['title', 'min_price', 'max_price', 'min_beds', 'min_baths', 'guests']