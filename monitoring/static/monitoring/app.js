init = () => {
    initMap();
    setInitials();
    connection = new Connection(onOpen, onMessage, onClose, onError);
}

onMessage = (msg) => {
    let event = JSON.parse(msg.data);
    const kind = event['kind'];
    const payload = event['payload'];
    console.log(`new event with kind ${kind} and payload ${JSON.stringify(payload)}`);
    if (kind === INITIAL) {
        onFullyConnected(payload);
    } else if (kind === TRACKERS) {
        let radios = document.querySelectorAll('input[type="radio"]');
        tracker_id=0;
        for (let radio of radios) {
            if (radio.checked) {
                tracker_id = radio.value;
            }
        }
        let c_lat = 0; let c_lon = 0;
        for (let tracker of payload['trackers']) {
            removeMark(tracker['tracker_id']);
            addMark(tracker['tracker_id'], tracker['lat'], tracker['lon'], tracker['tracker_name'], tracker['color']);
            if (Number(tracker_id) === tracker['id']) {   
                c_lat = tracker['lat'];
                c_lon = tracker['lon'];
            }
        }
        if (tracker_id>0){
            map.setCenter([c_lat, c_lon]);
        }
    } else if (kind === TRACK) {
        showTrack(payload['jsontrack'])
    } else if (kind === FILE) {
        get_file_url(payload['trackfile'])
    } else {
        console.log(`unsupported event kind ${kind}, data ${payload}`)
    }
}

get_file_url = (url) => {
	var link_url = document.createElement("a");
	link_url.download = url.substring((url.lastIndexOf("/") + 1), url.length);
	link_url.href = url;
	document.body.appendChild(link_url);
	link_url.click();
	document.body.removeChild(link_url);
	delete link_url;
}

onFullyConnected = (payload) => {
    id = payload['id'];
    connection.push(CONNECT_EVENT, {
        id: id, user_id: user_id, 
    });
    ping();
    timer = setInterval(ping, 10000);

}

ping = () => {
    if (!run) return;
    console.log(`ping`);
    connection.push(PING_EVENT, {
        id: id, user_id: user_id,
    });
}

getTrack = () => {
    if (!run) return;
    let radios = document.querySelectorAll('input[type="radio"]');
    start_date = document.getElementById("start_date").value;
    end_date = document.getElementById("end_date").value;
    tracker_id=0;
    for (let radio of radios) {
        if (radio.checked) {
            tracker_id = radio.value;
        }
    }
    if (tracker_id > 0){
        console.log(`get track`);
        connection.push(GET_TRACK, {
            id: id, 
            user_id: user_id, 
            tracker_id:tracker_id,
            start_date: start_date,
            end_date: end_date 
        });
    }
}

getFile = () => {
    if (!run) return;
    let radios = document.querySelectorAll('input[type="radio"]');
    start_date = document.getElementById("start_date").value;
    end_date = document.getElementById("end_date").value;
    tracker_id=0;
    for (let radio of radios) {
        if (radio.checked) {
            tracker_id = radio.value;
        }
    }
    if (tracker_id > 0){
        console.log(`get track`);
        connection.push(GET_FILE, {
            id: id, 
            user_id: user_id, 
            tracker_id:tracker_id,
            start_date: start_date,
            end_date: end_date 
        });
    }
}

onOpen = () => {
    console.log('ws connection opened');
}


onClose = () => {
    console.log('ws connection closed');
    connection.push(
        DISCONNECT_EVENT,
        {
            id: id,
        }
    );
    run = false;
    clearInterval(timer);
}


onError = (e) => {
    console.log(`connection closed with error ${e}`);
    run = false;
    clearInterval(timer);
}


setInitials = () => {
    if (!run) return;
    let radios = document.querySelectorAll('input[type="radio"]');
    start_date = document.getElementById("start_date");
    end_date = document.getElementById("end_date");
    start_date.valueAsDate = new Date();
    end_date.valueAsDate = new Date();   
    for (let radio of radios) {
        radio.checked = true;
        break;
    }

}