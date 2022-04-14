from typing import Dict
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic.base import View
from datetime import datetime, timedelta
from django.utils import timezone
import requests
from geopy.distance import geodesic as GD

from listenports.models import Tracks, Trackers
last_positions: Dict[int, Dict[str, float]] = {}


def bad_speed(last_pos, new_pos):
    res = False
    time = (new_pos['time']-last_pos['time']).total_seconds()
    distance = GD((last_pos['lat'], last_pos['lon']),
                  (new_pos['lat'], new_pos['lon'])).km
    speed = distance*1000/time
    new_pos['speed']=speed
    accel = (speed-last_pos['speed'])/time
    if (speed > 30)or(accel>3):
        res = True 
    return res


class ListenPortView(View):
    def post(self, request):
        try:
            tracker = Trackers.objects.get(tracker_id=request.GET['id'])
        except:
            return HttpResponseForbidden()
        dt = datetime.fromtimestamp(int(request.GET['timestamp']))
        new_datetime = timezone.make_aware(dt, timezone.utc)
        # Отбрасываем с низкой точностью
        if float(request.GET['accuracy']) > 20:
            return HttpResponse()
        #  Отбрасываем если нереальная скорость
        last_pos = last_positions.get(request.GET['id'])
        new_pos = {'lat': request.GET['lat'],
                   'lon': request.GET['lon'], 'time': new_datetime, 'speed': 0}
        if last_pos:
            if bad_speed(last_pos, new_pos):
                return HttpResponse()
        
        last_positions[request.GET['id']] = new_pos
        
        gps_point = Tracks()
        gps_point.tracker_id = request.GET['id']
        gps_point.tracker_m_id = tracker.id
        gps_point.lon = request.GET['lon']
        gps_point.lat = request.GET['lat']
        gps_point.alt = request.GET['altitude']
        gps_point.speed = request.GET['speed']
        gps_point.accuracy = request.GET['accuracy']
        gps_point.bearing = request.GET['bearing']
        gps_point.timestamp = new_datetime
        gps_point.save()

        if tracker.resend:
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
            _headers = {'User-Agent': 'TraccarClient'}
            response = requests.post(
                'http://livegpstracks.com', params=post_data, headers=_headers)

        return HttpResponse()

    def get(self, request):
        return HttpResponse("Listen gps track data")
