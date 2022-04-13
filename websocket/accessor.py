import json
import os
from datetime import datetime, timedelta
from asgiref.sync import sync_to_async
from dataclasses import asdict
import gpxpy as gpx
import gpxpy.gpx

from django.utils import timezone
from django.conf import settings

from listenports.models import Trackers
from django.contrib.auth.models import User
from .const import ServerEventKind, Event


@sync_to_async
def get_trackers(data: dict):
    user_id = data['user_id']
    trackers = []
    user = User.objects.get(pk=user_id)
    for tracker in user.trackers_set.all():
        tracker_d = {}
        tracker_d["id"] = tracker.pk
        tracker_d["tracker_id"] = tracker.tracker_id
        tracker_d["tracker_name"] = tracker.description
        try:
            pos = tracker.tracks.latest("timestamp")
            tracker_d["lon"] = pos.lon
            tracker_d["lat"] = pos.lat
            delta = (datetime.now() -
                     pos.timestamp.replace(tzinfo=None)).total_seconds()
            if delta < 60:
                tracker_d["color"] = "green"
            elif delta < 300:
                tracker_d["color"] = "yellow"
            else:
                tracker_d["color"] = "red"
        except:
            tracker_d["lon"] = 0
            tracker_d["lat"] = 0
            tracker_d["color"] = "red"

        trackers.append(tracker_d)

    event = Event(
        kind=ServerEventKind.TRACKERS,
        payload={
            'id': data['id'],
            'trackers': trackers,
        },
    )
    return json.dumps(asdict(event))


@sync_to_async
def get_track(data: dict):
    tracker_id = data['tracker_id']
    start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
    end_date = datetime.strptime(data['end_date'], "%Y-%m-%d")+timedelta(1)
    start_date = timezone.make_aware(start_date, timezone.utc)
    end_date = timezone.make_aware(end_date, timezone.utc)

    track = {}
    track["type"] = "FeatureCollection"
    tracker = Trackers.objects.get(pk=tracker_id)
    features = []
    id = 0
    line = {}
    line["type"] = "Feature"
    line["id"] = id
    line["geometry"] = {
        "type": "LineString",
    }
    coordinates =[]    
    for poi_db in tracker.tracks.filter(timestamp__range=[start_date, end_date]):
        coordinates.append([poi_db.lat, poi_db.lon])

    line["geometry"]["coordinates"] = coordinates
    line["options"] ={"strokeWidth": 3}

    features.append(line)

    track["features"] = features

    event = Event(
        kind=ServerEventKind.TRACK,
        payload={
            'id': data['id'],
            'jsontrack': track,
        },
    )
    return json.dumps(asdict(event))


@sync_to_async
def get_file(data: dict):
    tracker_id = data['tracker_id']
    start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
    end_date = datetime.strptime(data['end_date'], "%Y-%m-%d")+timedelta(1)
    start_date = timezone.make_aware(start_date, timezone.utc)
    end_date = timezone.make_aware(end_date, timezone.utc)

    gpx = gpxpy.gpx.GPX()
    tracker = Trackers.objects.get(pk=tracker_id)
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    for poi_db in tracker.tracks.filter(timestamp__range=[start_date, end_date]):
        gps_trackpoint = gpxpy.gpx.GPXTrackPoint(
            poi_db.lat,
            poi_db.lon,
            elevation=poi_db.alt,
            time=poi_db.timestamp,
            speed=poi_db.speed
        )
        gps_trackpoint.course = poi_db.bearing,
        gpx_segment.points.append(gps_trackpoint)

    f_track = open(os.path.join(settings.MEDIA_ROOT, 'track.gpx'), 'w')
    f_track.writelines(gpx.to_xml())
    f_track.close()

    event = Event(
        kind=ServerEventKind.FILE,
        payload={
            'id': data['id'],
            'trackfile': '/media/track.gpx',
        },
    )
    return json.dumps(asdict(event))
