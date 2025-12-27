from rest_framework import serializers
from .models import MaintenanceRequest
from equipment.models import Equipment
from teams.models import MaintenanceTeam
from django.contrib.auth import get_user_model

User = get_user_model()

class EquipmentBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('id', 'name', 'serial_number')

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    equipment = EquipmentBriefSerializer(read_only=True)
    equipment_id = serializers.PrimaryKeyRelatedField(queryset=Equipment.objects.all(), source='equipment', write_only=True)
    assigned_to = UserBriefSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='assigned_to', write_only=True, allow_null=True, required=False)

    class Meta:
        model = MaintenanceRequest
        fields = [
            'id', 'title', 'description', 'equipment', 'equipment_id', 'team', 'request_type',
            'scheduled_date', 'status', 'created_at', 'assigned_to', 'assigned_to_id', 'duration'
        ]
        read_only_fields = ('created_at',)
