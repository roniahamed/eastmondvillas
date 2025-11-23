# serializers.py
from rest_framework import serializers
from .models import Announcement, FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'file', 'created_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    # Nested read-only files for GET
    files = FileUploadSerializer(many=True, read_only=True)

    class Meta:
        model = Announcement
        fields = [
            'id',
            'title',
            'date',
            'priority',
            'description',
            'created_at',
            'updated_at',
            'files',
        ]
