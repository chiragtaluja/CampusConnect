from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("add-event/", views.add_event, name="add_event"),
    path("event/<str:event_id>/", views.event, name="event"),
    path("login/", views.user_login, name="user_login"),
    path("admin_dashboard/<str:admin_id>/", views.admin , name="admin_dashboard"),
    path("logout/", views.user_logout , name="logout")
]