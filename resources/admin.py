from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline 

# Register your models here.
from .models import Resource, ResourceMedia


class ResourceMediaInline(TabularInline):
    model = ResourceMedia
    extra = 1


admin.site.register(Resource)
class ResourceAdmin(ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'category')
    list_filter = ('category', 'created_at', 'updated_at')
    inlines = [ResourceMediaInline]


admin.site.register(ResourceMedia)


class ResourceMediaAdmin(ModelAdmin):
    list_display = ('resource', 'file')
