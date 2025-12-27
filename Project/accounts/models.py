from django.db import models
from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[
        ('overdue', 'Overdue Maintenance'),
        ('upcoming', 'Upcoming Maintenance'),
        ('new_request', 'New Request'),
        ('status_change', 'Status Change'),
        ('system', 'System Notification'),
    ])
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)  # ID of related object (equipment, request, etc.)
    related_model = models.CharField(max_length=50, null=True, blank=True)  # Model name

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"

class UserSettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    theme = models.CharField(max_length=20, default='light')
    notifications = models.BooleanField(default=True)

    # ✅ ADD THIS
    preferences = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Settings"

    theme = models.CharField(max_length=20, default='light')
    notifications = models.BooleanField(default=True)

    # ✅ ADD THIS
    preferences = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Settings"
