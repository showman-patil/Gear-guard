from django.shortcuts import render, get_object_or_404
from equipment.models import Equipment

def dashboard(request):
    return render(request, 'dashboard.html')

def kanban_board(request):
    requests = MaintenanceRequest.objects.select_related("equipment", "technician")
    return render(request, "maintenance/kanban.html", {"requests": requests})
