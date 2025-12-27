from django.contrib import admin
from .models import MaintenanceRequest


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
	list_display = ('title', 'equipment', 'team', 'status', 'assigned_to', 'created_at')
	list_filter = ('status', 'request_type', 'team')
	search_fields = ('title', 'description', 'equipment__name')
