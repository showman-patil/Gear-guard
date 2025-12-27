from django.db import models
from teams.models import MaintenanceTeam

class Equipment(models.Model):
    name = models.CharField(max_length=150)
    serial_number = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=150)

    # ✅ FIXED: Now proper relation
    maintenance_team = models.ForeignKey(
        MaintenanceTeam,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('scrap', 'Scrap')],
        default='active'
    )

    purchase_date = models.DateField(blank=True, null=True)
    warranty_end = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
