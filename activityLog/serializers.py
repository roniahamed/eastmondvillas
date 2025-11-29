from rest_framework import serializers
from auditlog.models import LogEntry
import json

from rest_framework import serializers
from auditlog.models import LogEntry

class LogEntrySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    detials = serializers.SerializerMethodField()


    class Meta:
        model = LogEntry
        fields = ['user','action','timestamp','type','detials'] 

    def get_user(self, obj):
        if obj.actor:
            return str(obj.actor)

        changes = obj.changes or {}
        
        if isinstance(changes, str):
            try:
                changes = json.loads(changes)
            except ValueError:
                return None

        data_entry = changes.get("data")
        if data_entry and isinstance(data_entry, list) and len(data_entry) > 1:
            new_value = data_entry[1]

            if isinstance(new_value, str):
                try:
                    data_dict = json.loads(new_value)
                    if isinstance(data_dict, dict):
                        return data_dict.get("name")
                except (json.JSONDecodeError, TypeError):
                    return None
            
        return None

    def get_action(self, obj):
        action_map = {
            0: "Created",
            1: "Updated",
            2: "Deleted",
        }
        return action_map.get(obj.action, "Unknown")
    def get_timestamp(self, obj):
        return obj.timestamp.strftime("%Y-%m-%d %H:%M")
    def get_type(self, obj):
        type_map = {
            0: "upload",
            1: "edit",
            2: "delete",
        }
        return type_map.get(obj.action, "other")
    def get_detials(self, obj):
        return obj.object_repr