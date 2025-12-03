from rest_framework import serializers
from .models import Resource, ResourceMedia


class ResourceMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceMedia
        fields = ['id', 'file']

class ResourceSerializer(serializers.ModelSerializer):
    files = ResourceMediaSerializer(source="media_resources", many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    class Meta:
        model = Resource
        fields = ['id', 'title', 'category', 'description', 'files', 'updated_at', 'created_at', 'uploaded_files']
        read_only_fields = ['updated_at', 'created_at', 'files']
    
    def create(self, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        resource = Resource.objects.create(**validated_data)
        for file in uploaded_files:
            ResourceMedia.objects.create(resource=resource, file=file)
        return resource