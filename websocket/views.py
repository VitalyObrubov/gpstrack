import uuid
import json
from dataclasses import asdict

from django.views.generic.base import TemplateView

from .connection import WebSocket
from .accessor import get_file, get_track, get_trackers
from .const import ServerEventKind, ClientEventKind, Event

def connect_answer():
    connection_id = uuid.uuid4()
    event=Event(
        kind=ServerEventKind.INITIAL,
        payload={
            'id': str(connection_id),               
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
        if message['kind'] == ClientEventKind.GET_TRACK:
            answ = await get_track(message['data'])
        if message['kind'] == ClientEventKind.GET_FILE:
            answ = await get_file(message['data'])

        await socket.send_text(answ)


class IndexView(TemplateView):
    template_name = "index.html"