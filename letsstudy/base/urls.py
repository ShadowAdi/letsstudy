from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("", views.Home, name="Home"),
    path("room/<str:pk>", views.RoomView, name="room"),
    path("create-room/", views.createRoom, name="room-form"),
    path("update-room/<str:pk>", views.updateRoom, name="update-form"),
    path("delete-room/<str:pk>", views.deleteRoom, name="delete-form"),
    path("delete-message/<str:pk>", views.deleteMessage, name="delete-message"),
    path("profile/<str:pk>", views.userProfile, name="profile"),
    path("editUser/", views.updateUser, name="updateUser"),
    path("topics/", views.topicsPage, name="topics"),
    path("activity/", views.activitiesPage, name="activity"),

]
