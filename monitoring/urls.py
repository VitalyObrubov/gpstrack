from django.urls import path
from .views import IndexView, TrackerCreateView

urlpatterns = [
    path('', IndexView.as_view(), name = 'monitoring'),
    path('add/', TrackerCreateView.as_view (), name='add_tracker') ,

]
