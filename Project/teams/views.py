from django.shortcuts import render, redirect
from .models import MaintenanceTeam
from .forms import MaintenanceTeamForm

def team_list(request):
    teams = MaintenanceTeam.objects.all()
    return render(request, 'teams/team_list.html', {'teams': teams})


def team_add(request):
    if request.method == "POST":
        form = MaintenanceTeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = MaintenanceTeamForm()

    return render(request, 'teams/team_form.html', {'form': form})
