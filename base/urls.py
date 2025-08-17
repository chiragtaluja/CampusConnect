from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("add-event/", views.add_event, name="add_event"),
    path("event/<str:event_id>/", views.event, name="event"),
]
