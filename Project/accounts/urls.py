from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("api/profile/", views.profile_api, name="profile_api"),
    path("settings/", views.settings_view, name="settings"),
    path("api/settings/", views.settings_api, name="settings_api"),
    path("api/notifications/", views.notifications_api, name="notifications_api"),
    path("api/notifications/<int:notification_id>/read/", views.mark_notification_read, name="mark_notification_read"),
    path("api/notifications/mark_all_read/", views.mark_all_notifications_read, name="mark_all_notifications_read"),

]
