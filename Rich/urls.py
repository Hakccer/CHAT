from django.contrib import admin
from django.urls import path, include
from Rich import views

urlpatterns = [
    path("", views.home, name="My Home"),
    path("rooms/message", views.sender, name="Sends"),
    path("rooms/messages", views.getter, name="message"),
    path("rooms/leave", views.leave, name="leave"),
    path("rooms/<slug:slug>", views.handle, name="Room")
]
