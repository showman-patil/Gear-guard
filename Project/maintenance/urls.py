from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.maintenance_create, name='maintenance_add'),
    path('kanban/', views.kanban_board, name='kanban_board'),
    
    # API endpoints for nban
    path('api/kanban/', views.kanban_api, name='kanban_api'),
    path('api/requests/<int:pk>/status/', views.update_request_status, name='update_request_status'),
    path('api/dashboard/', views.dashboard_data, name='dashboard_data'),
    path('api/notifications/', views.notifications_api, name='notifications_api'),
    path('api/notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
]
