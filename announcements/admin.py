from django.contrib import admin
from .models import Announcement, FileUpload

admin.site.register(Announcement)
admin.site.register(FileUpload)

