from django.urls import path
from . import views


urlpatterns = [
    path("", views.getRoutes, name="single"),
    path("rooms/", views.getRooms, name="rooms"),
]
