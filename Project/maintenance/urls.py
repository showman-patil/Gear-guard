from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.maintenance_create, name='maintenance_add'),
    path('kanban/', views.kanban_board, name='kanban_board'),
    # API endpoints for kanban
    path('api/kanban/', views.kanban_api, name='kanban_api'),
    path('api/requests/<int:pk>/status/', views.update_request_status, name='update_request_status'),
]
