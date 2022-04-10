from django.urls import path
from websocket import views

websocket = path

urlpatterns = [
    path("", views.IndexView.as_view()),
    websocket("connect/", views.websocket_view),
]