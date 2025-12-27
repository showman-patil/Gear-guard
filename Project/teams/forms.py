from django import forms
from .models import MaintenanceTeam

class MaintenanceTeamForm(forms.ModelForm):
    class Meta:
        model = MaintenanceTeam
        fields = ['name', 'description']
