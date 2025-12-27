from django.db import models
from django.conf import settings


class MaintenanceTeam(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='maintenance_teams')

    def __str__(self):
        return self.name

