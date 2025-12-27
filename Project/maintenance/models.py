from django.db import models
from django.conf import settings
from equipment.models import Equipment
from teams.models import MaintenanceTeam

class MaintenanceRequest(models.Model):

    REQUEST_TYPE = (
        ('corrective', 'Corrective (Breakdown)'),
        ('preventive', 'Preventive (Routine)'),
    )

    STATUS_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('repaired', 'Repaired'),
        ('scrap', 'Scrap'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE
    )

    team = models.ForeignKey(
        MaintenanceTeam,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPE
    )

    scheduled_date = models.DateField(null=True, blank=True)

    # technician assigned to the request (optional)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_requests'
    )

    # duration in hours (set when work is completed)
    duration = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
