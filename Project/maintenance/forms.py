from django import forms
from .models import MaintenanceRequest

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = [
            'title',
            'description',
            'equipment',
            'status',
            'request_type',
            'scheduled_date'
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Short descriptive title'}),
            'description': forms.Textarea(attrs={'class': 'field', 'rows': 3, 'placeholder': 'What happened?'}),
            'scheduled_date': forms.DateInput(attrs={'type': 'date', 'class': 'field'}),
            'request_type': forms.Select(attrs={'class': 'field'}),
            'equipment': forms.Select(attrs={'class': 'field'}),
        }
