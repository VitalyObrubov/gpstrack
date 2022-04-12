from dataclasses import dataclass

class ServerEventKind:
    INITIAL = 'initial'
    TRACKERS = 'trackers'
    TRACK = 'track'
    FILE = 'file'

class ClientEventKind:
    CONNECT = 'connect'
    PING = 'ping'
    GET_TRACK = 'get_track'
    GET_FILE = 'get_file'
    DISCONNECT = 'disconnect'


@dataclass
class Event:
    kind: str
    payload: dict