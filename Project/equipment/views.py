from django.shortcuts import render, get_object_or_404, redirect
from .models import Equipment
from .forms import EquipmentForm

def equipment_list(request):
    equipments = Equipment.objects.all().order_by('-id')
    return render(request, 'equipment/equipment_list.html', {
        'equipments': equipments
    })

def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    return render(request, 'equipment/equipment_detail.html', {
        'equipment': equipment
    })

def equipment_create(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm()

    return render(request, 'equipment/equipment_form.html', {
        'form': form
    })

def equipment_edit(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)

    if request.method == "POST":
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm(instance=equipment)

    return render(request, 'equipment/equipment_form.html', {
        'form': form,
        'edit': True
    })

def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment.delete()
    return redirect('equipment_list')

