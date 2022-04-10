import uuid
import json
import datetime as dt
from datetime import datetime,timedelta
from dataclasses import asdict, dataclass
from asgiref.sync import sync_to_async

from django.utils import timezone
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User


from .connection import WebSocket
from listenports.models import Trackers

class ServerEventKind:
    INITIAL = 'initial'
    TRACKERS = 'trackers'
    TRACK = 'track'

class ClientEventKind:
    CONNECT = 'connect'
    PING = 'ping'
    GET_TRACK = 'get_track'
    DISCONNECT = 'disconnect'

@dataclass
class Event:
    kind: str
    payload: dict



def connect_answer():
    connection_id = uuid.uuid4()
    event=Event(
        kind=ServerEventKind.INITIAL,
        payload={
            'id': str(connection_id),               
        },
    )
    return json.dumps(asdict(event))

@sync_to_async  
def get_trackers(data: dict): 
    user_id = data['user_id']
    trackers = []
    user = User.objects.get(pk=user_id)
    for tracker in user.trackers_set.all():
        tracker_d = {}
        tracker_d["tracker_id"] = tracker.tracker_id
        tracker_d["tracker_name"] = tracker.description
        try:
            pos = tracker.tracks.latest("timestamp")
            tracker_d["lon"] = pos.lon
            tracker_d["lat"] = pos.lat
            delta = (datetime.now()- pos.timestamp.replace(tzinfo=None)).total_seconds()
            if delta<60:
                tracker_d["color"] = "green" 
            elif delta<300:
                tracker_d["color"] = "yellow" 
            else:
                tracker_d["color"] = "red" 
        except:
            tracker_d["lon"] = 0
            tracker_d["lat"] = 0
            tracker_d["color"] = "red"  

        trackers.append(tracker_d)
    
    event=Event(
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
    prev_poi = None
    for poi_db in tracker.tracks.filter(timestamp__range = [start_date,end_date]):
        if prev_poi == None:
            prev_poi = poi_db
            continue
        id += 1
        poi = {}
        poi["type"] = "Feature"
        poi["id"] = id
        poi["geometry"] = {
            "type": "LineString",
            "coordinates": [
                [prev_poi.lat, prev_poi.lon],
                [poi_db.lat, poi_db.lon]
            ]
        }
        features.append(poi)

        prev_poi = poi_db
    track["features"] = features
    
    event=Event(
        kind=ServerEventKind.TRACK,
        payload={
            'id': data['id'], 
            'jsontrack': track,              
        },
    )
    return json.dumps(asdict(event))


async def websocket_view(socket:WebSocket):
    await socket.accept()
    answ = connect_answer()
    await socket.send_text(answ)

    while True:
        raw_message = await socket.receive_text()
        message = json.loads(raw_message)
        if message['kind'] == ClientEventKind.PING:
            answ = await get_trackers(message['data'])
            #print("ping  " + datetime.now().strftime("%H:%M:%S"))
        if message['kind'] == ClientEventKind.GET_TRACK:
            answ = await get_track(message['data'])

        await socket.send_text(answ)


class IndexView(TemplateView):
    template_name = "index.html"