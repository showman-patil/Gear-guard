from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import MaintenanceRequestForm
from .models import MaintenanceRequest
from equipment.models import Equipment

# DRF imports for API endpoints
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import MaintenanceRequestSerializer

def maintenance_create(request):
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)

            # ✅ ONLY ONE SOURCE OF TRUTH
            equipment = maintenance.equipment

            if equipment.maintenance_team:
                maintenance.team = equipment.maintenance_team
            else:
                maintenance.team = None  # safe fallback

            maintenance.save()
            return redirect('kanban_board')
    else:
        form = MaintenanceRequestForm()

    equipments = Equipment.objects.all()

    return render(request, 'maintenance/maintenance_form.html', {
        'form': form,
        'equipments': equipments
    })

@login_required
def kanban_board(request):
    # main kanban page (html + client-side JS will fetch API data)
    return render(request, 'maintenance/kanban.html')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kanban_api(request):
    """Return kanban items grouped by status"""
    qs = MaintenanceRequest.objects.select_related('equipment', 'assigned_to', 'team').all().order_by('created_at')
    serializer = MaintenanceRequestSerializer(qs, many=True)
    grouped = {'new': [], 'in_progress': [], 'repaired': [], 'scrap': []}
    for item in serializer.data:
        grouped[item['status']].append(item)
    return Response(grouped)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_request_status(request, pk):
    """Update a request status with validation"""
    req = get_object_or_404(MaintenanceRequest, pk=pk)
    new_status = request.data.get('status')
    # allowed transitions
    allowed = {
        'new': ['in_progress', 'scrap'],
        'in_progress': ['repaired', 'scrap'],
        'repaired': [],
        'scrap': [],
    }
    if new_status not in [c[0] for c in MaintenanceRequest.STATUS_CHOICES]:
        return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    if new_status not in allowed.get(req.status, []):
        return Response({'detail': f'Invalid transition from {req.status} to {new_status}'}, status=status.HTTP_400_BAD_REQUEST)

    # If marking as repaired, ensure duration provided
    if new_status == 'repaired' and not request.data.get('duration'):
        return Response({'detail': 'Duration required when marking repaired.'}, status=status.HTTP_400_BAD_REQUEST)

    # apply updates
    if 'assigned_to' in request.data:
        # set assigned technician if provided
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if request.data['assigned_to']:
            user = get_object_or_404(User, pk=request.data['assigned_to'])
            req.assigned_to = user
        else:
            req.assigned_to = None

    if 'duration' in request.data:
        req.duration = request.data.get('duration')

    req.status = new_status
    req.save()

    # If scrap, mark equipment status
    if new_status == 'scrap':
        eq = req.equipment
        eq.status = 'scrap'
        eq.save()

    return Response(MaintenanceRequestSerializer(req).data)