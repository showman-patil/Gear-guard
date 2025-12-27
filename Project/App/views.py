from django.shortcuts import render, get_object_or_404
from equipment.models import Equipment
from maintenance.models import MaintenanceRequest
from teams.models import MaintenanceTeam
from accounts.models import Notification
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.models import User
import json

def dashboard(request):
    # KPI data
    total_equipment = Equipment.objects.count()
    total_requests = MaintenanceRequest.objects.count()
    in_progress = MaintenanceRequest.objects.filter(status='in_progress').count()
    scrap_equipment = Equipment.objects.filter(status='scrap').count()
    
    # Overdue: requests with scheduled_date in the past and not completed
    overdue = MaintenanceRequest.objects.filter(
        scheduled_date__lt=timezone.now().date(),
        status__in=['new', 'in_progress']
    ).count()
    
    # Chart data: status counts
    status_counts = MaintenanceRequest.objects.values('status').annotate(count=Count('status'))
    status_data = {item['status']: item['count'] for item in status_counts}
    
    # Overdue list
    overdue_requests = MaintenanceRequest.objects.filter(
        scheduled_date__lt=timezone.now().date(),
        status__in=['new', 'in_progress']
    ).select_related('equipment', 'assigned_to').order_by('scheduled_date')[:10]  # Limit to 10
    
    overdue_list = []
    for req in overdue_requests:
        overdue_list.append({
            'eq': req.equipment.name,
            'tech': req.assigned_to.get_full_name() if req.assigned_to else '-',
            'date': req.scheduled_date.strftime('%b %d, %Y') if req.scheduled_date else '-'
        })
    
    # Create notifications for overdue requests
    for req in overdue_requests:
        # Check if notification already exists
        exists = Notification.objects.filter(
            user=request.user,
            notification_type='overdue',
            related_object_id=req.id,
            related_model='MaintenanceRequest'
        ).exists()
        if not exists:
            Notification.objects.create(
                user=request.user,
                title=f"Overdue: {req.title}",
                message=f"Maintenance request for {req.equipment.name} is overdue (due: {req.scheduled_date})",
                notification_type='overdue',
                related_object_id=req.id,
                related_model='MaintenanceRequest'
            )
    
    # Upcoming preventive maintenance
    upcoming_requests = MaintenanceRequest.objects.filter(
        request_type='preventive',
        scheduled_date__gte=timezone.now().date(),
        status='new'
    ).select_related('equipment').order_by('scheduled_date')[:10]
    
    upcoming_list = []
    for req in upcoming_requests:
        upcoming_list.append({
            'eq': req.equipment.name,
            'date': req.scheduled_date.strftime('%b %d, %Y') if req.scheduled_date else '-'
        })
    
    # Create notifications for upcoming requests
    for req in upcoming_requests:
        # Check if notification already exists
        exists = Notification.objects.filter(
            user=request.user,
            notification_type='upcoming',
            related_object_id=req.id,
            related_model='MaintenanceRequest'
        ).exists()
        if not exists:
            Notification.objects.create(
                user=request.user,
                title=f"Upcoming: {req.title}",
                message=f"Preventive maintenance for {req.equipment.name} is scheduled for {req.scheduled_date}",
                notification_type='upcoming',
                related_object_id=req.id,
                related_model='MaintenanceRequest'
            )
    
    # Team workload
    team_workload = MaintenanceRequest.objects.filter(
        status__in=['new', 'in_progress']
    ).values('team__name').annotate(count=Count('id')).order_by('-count')
    
    teams_data = {}
    colors = ['blue', 'green', 'purple', 'indigo', 'red', 'yellow']
    color_index = 0
    for item in team_workload:
        team_name = item['team__name'] or 'Unassigned'
        teams_data[team_name] = {
            'count': item['count'],
            'color': colors[color_index % len(colors)]
        }
        color_index += 1
    
    context = {
        'total_equipment': total_equipment,
        'total_requests': total_requests,
        'in_progress': in_progress,
        'overdue': overdue,
        'scrap_equipment': scrap_equipment,
        'status_data': status_data,
        'overdue_list_json': json.dumps(overdue_list),
        'upcoming_list_json': json.dumps(upcoming_list),
        'teams_data_json': json.dumps(teams_data),
    }
    return render(request, 'dashboard.html', context)

def kanban_board(request):
    requests = MaintenanceRequest.objects.select_related("equipment", "assigned_to")
    return render(request, "maintenance/kanban.html", {"requests": requests})
