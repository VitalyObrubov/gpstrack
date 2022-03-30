from django.http import HttpResponse 
from django.views.generic.base import View
from datetime import datetime
from django.utils import timezone
import requests

from listenports.models import Tracks

class ListenPortView(View):
    def post(self, request):
        dt = datetime.fromtimestamp(int(request.GET['timestamp']))
        new_datetime = timezone.make_aware(dt, timezone.utc)       
        gps_point = Tracks()
        gps_point.tracker_id = request.GET['id']
        gps_point.lon = request.GET['lon']
        gps_point.lat = request.GET['lat']
        gps_point.alt = request.GET['altitude']
        gps_point.speed = request.GET['speed']
        gps_point.accuracy = request.GET['accuracy']
        gps_point.bearing = request.GET['bearing']
        gps_point.timestamp = new_datetime
        gps_point.save()

        post_data = {
            'id': request.GET['id'],
            'timestamp': request.GET['timestamp'],
            'lon': request.GET['lon'],
            'lat': request.GET['lat'],
            'altitude': request.GET['altitude'],
            'speed': request.GET['speed'],
            'accuracy': request.GET['accuracy'],
            'bearing': request.GET['bearing'],
            'batt': request.GET['batt'],
        }
        _headers = {'User-Agent':'TraccarClient'}
        response = requests.post('http://livegpstracks.com', params=post_data, headers=_headers)
        #response = requests.post('http://127.0.0.1:8000', params=post_data)
        content = response.content

        return HttpResponse()

    def get(self, request): 
        q=0
        return HttpResponse("Listen gps track data")