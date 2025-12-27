from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            'name',
            'serial_number',
            'department',
            'location',
            'maintenance_team',
            'purchase_date',
            'warranty_end',
            'status'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'field'}),
            'serial_number': forms.TextInput(attrs={'class': 'field'}),
            'department': forms.TextInput(attrs={'class': 'field'}),
            'location': forms.TextInput(attrs={'class': 'field'}),
            'maintenance_team': forms.Select(attrs={'class': 'field'}),
            'status': forms.Select(attrs={'class': 'field'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': 'field'}),
            'warranty_end': forms.DateInput(attrs={'type': 'date', 'class': 'field'}),
        }
