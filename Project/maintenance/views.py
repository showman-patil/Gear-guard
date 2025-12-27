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

# Add Notification import
from accounts.models import Notification

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

# Dashboard data endpoint
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
from teams.models import MaintenanceTeam
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_data(request):
    """Return dashboard metrics and small lists as JSON."""
    today = timezone.localdate()

    total_equipment = Equipment.objects.count()
    requests = MaintenanceRequest.objects.all()

    overdue_qs = MaintenanceRequest.objects.filter(scheduled_date__lt=today).exclude(status__in=['repaired','scrap']).select_related('equipment','assigned_to')[:10]
    overdue_list = [
        { 'eq': str(r.equipment), 'tech': (r.assigned_to.username if r.assigned_to else None), 'date': (r.scheduled_date.isoformat() if r.scheduled_date else None) }
        for r in overdue_qs
    ]

    upcoming_qs = MaintenanceRequest.objects.filter(scheduled_date__gte=today).order_by('scheduled_date').select_related('equipment')[:10]
    upcoming_list = [ {'eq': str(r.equipment), 'date': (r.scheduled_date.isoformat() if r.scheduled_date else None)} for r in upcoming_qs ]

    team_counts = MaintenanceRequest.objects.values('team__name').annotate(count=Count('id')).order_by('-count')
    teams = { t['team__name'] or 'Unassigned': {'count': t['count']} for t in team_counts }

    # Generate notifications for overdue items
    _generate_overdue_notifications(request.user, overdue_qs)

    data = {
        "equipment": total_equipment,
        "requests": requests.count(),
        "inProgress": requests.filter(status="in_progress").count(),
        "overdue": overdue_qs.count(),
        "scrap": Equipment.objects.filter(status="scrap").count(),
        "status": {
            "new": requests.filter(status="new").count(),
            "in_progress": requests.filter(status="in_progress").count(),
            "repaired": requests.filter(status="repaired").count(),
            "scrap": requests.filter(status="scrap").count(),
        },
        'overdueList': overdue_list,
        'upcoming': upcoming_list,
        'teams': teams
    }

    return JsonResponse(data)

def _generate_overdue_notifications(user, overdue_requests):
    """Generate notifications for overdue maintenance requests"""
    for req in overdue_requests:
        # Check if notification already exists
        exists = Notification.objects.filter(
            user=user,
            notification_type='overdue',
            related_object_id=req.id,
            related_model='MaintenanceRequest'
        ).exists()
        if not exists:
            Notification.objects.create(
                user=user,
                title=f"Overdue Maintenance: {req.equipment}",
                message=f"Maintenance request for {req.equipment} is overdue. Scheduled date: {req.scheduled_date}",
                notification_type='overdue',
                related_object_id=req.id,
                related_model='MaintenanceRequest'
            )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notifications_api(request):
    """Return user notifications"""
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')[:20]
    data = [{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'type': n.notification_type,
        'is_read': n.is_read,
        'created_at': n.created_at.isoformat(),
        'related_object_id': n.related_object_id,
        'related_model': n.related_model,
    } for n in notifications]
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, pk):
    """Mark a notification as read"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return Response({'status': 'ok'})
