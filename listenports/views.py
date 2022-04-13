from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic.base import View
from datetime import datetime
from django.utils import timezone
import requests

from listenports.models import Tracks, Trackers


class ListenPortView(View):
    def post(self, request):
        try:
            tracker = Trackers.objects.get(tracker_id=request.GET['id'])
        except:
            return HttpResponseForbidden()

        dt = datetime.fromtimestamp(int(request.GET['timestamp']))
        new_datetime = timezone.make_aware(dt, timezone.utc)
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
