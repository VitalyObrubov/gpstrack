class Connection {
    constructor(onOpen, onMessage, onClose, onError) {
        this.connection = new WebSocket(path);
        this.connection.onmessage = onMessage;
        this.connection.onclose = onClose;
        this.connection.onerror = onError;
        this.connection.onopen = onOpen;
    }

    push = (kind, data) => {
        this.connection.send(JSON.stringify({kind: kind, data: data}));
    }
}


