from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("add_event/", views.add_event, name="add_event"),
    path("event/<int:event_id>/", views.event, name="event"),
    path("login/", views.user_login, name="user_login"),
    path("admin_dashboard/<int:admin_id>/", views.admin_dashboard , name="admin_dashboard"),
    path("logout/", views.user_logout , name="logout")
]