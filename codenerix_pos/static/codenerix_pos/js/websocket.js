function CodenerixPOSWebsocket(url, path, uuid, key) {

    // Initialize class
    var self = this;
    self.socket = null;
    self.debug_name = null
    self.debug_config = null;
    self.url = url;
    self.path = path;
    self.encrypt = false;
    self.uuid = uuid;
    self.key = key;

    // Set debugger system
    self.set_name = function (name) {
        self.debug_name = name;
    };
    self.set_debug = function (config) {
        self.debug_config = true;
    }
    self.warning = function(msg) {
        console.warn(self.debug_name+" - " + msg);
    }
    self.error = function(msg) {
        console.error(self.debug_name+" - " + msg);
    }
    self.debug = function(msg) {
        if (self.debug_config != null) {
            console.log(self.debug_name+" - " + msg);
        }
    }

    // Start WebSocket
    self.start = function () {

        // When we're using HTTPS, use WSS too.
        var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
        var ws_path = ws_scheme + '://'+self.url+'/'+self.path;

        // Connect to the remote server
        self.debug("Starting CodenerixPOS :: "+"Connecting to " + ws_path)
        // self.socket = new ReconnectingWebSocket(ws_path);
        self.socket = new ReconnectingWebSocket(ws_path);

        // Set onopen
        self.socket.onopen = function() {
            if (self.socket != null) {
                self.debug("Opened");
                if (typeof(self.opened)!='undefined') {
                    self.opened();
                }
            } else {
                self.error("Socket not available!");
            }
        };

        // Set default onmessage to websocket
        self.socket.onmessage = function(message) {
            self.debug("New message arrived: " + message.data);
            if (typeof(message.data) == 'undefined') {
                self.send_error("Missing 'data'");
            } else if (message.data != null) {
                self.received_message(message.data);
            } else {
                self.send_error("'data' is null");
            }
        };

        // Set onclose
        self.socket.onclose = function() {
            self.debug("Closed");
            if (typeof(self.closed)!='undefined') {
                self.closed();
            }
        };
    };

    // Send message
    self.send = function (request, ref) {
        if (typeof(request) != 'undefined') {
            if (typeof(ref) != 'undefined') {
                if (self.socket != null) {
                    // Encode request
                    var msg = JSON.stringify({'request': request, 'ref': ref});

                    // Build query
                    var query = {
                        'uuid': self.uuid,
                        'message': encrypt(msg, self.key),
                    };

                    // Encode to JSON
                    var data = JSON.stringify(query);

                    // Send to remote
                    self.socket.send(data);
                } else {
                    self.error("Socket is not open!");
                }
            } else {
                self.error("REF parameter can not be undefined, you must provide something or null");
            }
        } else {
            self.error("REQUEST parameter can not be undefined");
        }
    };

    // Send error
    self.send_error = function (msg, ref, uid) {
        if (typeof(ref) == 'undefined') {
            ref = null;
        }
        if (typeof(uid) == 'undefined') {
            uid = null;
        }
        if (self.socket != null) {
            self.error(msg+" (ref:"+ref+")");
            var msg = {'action':'error', 'error':msg};
            if (typeof(uid) != 'undefined') {
                msg['uuid'] = uid;
            }
            if (self.encrypt) {
                self.send(msg, ref);
            } else {
                self.socket.send(JSON.stringify({'message': msg}));
            }
        } else {
            self.error("Socket is not open!");
        }
    };

    // Received message
    self.received_message = function (pack) {
        try {
            request = JSON.parse(pack);
        } catch(e) {
            request = null;
        }

        // Check if we got a message
        if ( (request != null) && (typeof(request) == 'object') ) {
            message = request.message;
            if (typeof(message) == 'undefined') {
                self.send_error("Missing 'message'");
            } else if (message != null) {

                // Decrypt the message
                try {
                    msg = decrypt(message, self.key);
                    if (msg.length>0) {
                        self.encrypt = true;
                    } else {
                        msg = message;
                    }
                } catch (e) {
                    self.warning("Message is not encrypted or we have the wrong KEY");
                    msg = message;
                }
                try {
                    query = JSON.parse(msg);
                } catch (e) {
                    query = null;
                }

                if ( (query != null) && (typeof(query) == 'object') ) {
                    request = query.request;
                    if ( (typeof(request) != 'undefined') && (request != null) ) {
                        ref = query.ref;
                        if (typeof(ref) != 'undefined') {
                            if (typeof(request) == 'object') {
                                self.debug("Receive: "+JSON.stringify(request));
                                if (typeof(self.recv)!='undefined') {
                                    self.recv(request, ref);
                                } else {
                                    console.error("No 'recv' method found, I can not do anything with this request!");
                                }
                            } else {
                                self.send_error("Message is not a Dictionary", ref);
                            }
                        } else {
                            self.error("REF is missing in the query");
                        }
                    } else {
                        if (query.action == 'pong') {
                            self.warning("PONG "+query.ref)
                        } else {
                            self.error("Message doesn't belong to CODENERIX POS")
                        }
                    }
                } else if (query == null) {
                    self.send_error("Message is not JSON or is null");
                } else {
                    self.send_error("Message doesn't look like a dictionary");
                }

            } else {
                self.send_error("'message' is null");
            }

        } else {

            if (request == null) {
                self.send_error("Request is not JSON or is null");
            } else {
                self.send_error("Request doesn't look like a dictionary");
            }

        }
    }

    // Stop Websocket
    self.stop = function () {
        if (self.socket != null) {
            self.debug("Closing socket!")
            self.socket.close();
            self.socket = null;
        } else {
            self.warning("Socket already closed!");
        }
    }

    // Alias
    self.open = function() {
        self.start();
    }
    self.close = function() {
        self.stop();
    }

}
