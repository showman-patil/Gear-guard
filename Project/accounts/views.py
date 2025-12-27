from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django import forms
from maintenance.models import MaintenanceRequest

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm = request.POST["confirm"]

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("signup")

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect("dashboard")   # change to your dashboard route

    return render(request, "accounts/signup.html")
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "accounts/login.html")
def logout_view(request):
    logout(request)
    return redirect("login")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "mt-1 w-full px-4 py-2 rounded-lg border border-gray-200"}),
            'last_name': forms.TextInput(attrs={"class": "mt-1 w-full px-4 py-2 rounded-lg border border-gray-200"}),
            'email': forms.EmailInput(attrs={"class": "mt-1 w-full px-4 py-2 rounded-lg border border-gray-200"}),
        }


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = ProfileForm(instance=user)

    # Teams (if teams app defines maintenance_teams m2m)
    teams = getattr(user, 'maintenance_teams', None)
    user_teams = teams.all() if teams is not None else []

    # Assigned open requests
    assigned_open = MaintenanceRequest.objects.filter(assigned_to=user, status__in=['new', 'in_progress'])
    assigned_closed = MaintenanceRequest.objects.filter(assigned_to=user).exclude(status__in=['new', 'in_progress'])

    context = {
        'form': form,
        'user_obj': user,
        'teams': user_teams,
        'assigned_open': assigned_open,
        'assigned_closed': assigned_closed,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def settings_view(request):
    # simple settings page - expand later with persistent user prefs
    if request.method == 'POST':
        # For now, just save a theme preference to session as an example
        theme = request.POST.get('theme', 'auto')
        request.session['theme'] = theme
        messages.success(request, 'Settings saved')
        return redirect('settings')

    current_theme = request.session.get('theme', 'auto')
    # Render the existing project-level settings template (templates/setting.html)
    return render(request, 'setting.html', {'current_theme': current_theme})
