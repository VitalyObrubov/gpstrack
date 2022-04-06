from django.urls import path
from .views import IndexView, TrackerCreateView, MonitoringView

urlpatterns = [
    path('', MonitoringView.as_view(), name = 'monitoring'),
    path('add/', TrackerCreateView.as_view (), name='add_tracker') ,

]
