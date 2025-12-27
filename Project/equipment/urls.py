from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('add/', views.equipment_create, name='equipment_add'),
    path('<int:pk>/edit/', views.equipment_edit, name='equipment_edit'),
    path('<int:pk>/delete/', views.equipment_delete, name='equipment_delete'),
    path('<int:pk>/', views.equipment_detail, name='equipment_detail'),
]

