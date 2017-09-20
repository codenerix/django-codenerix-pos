var uuid_websocket = undefined;
var key_websocket = undefined;
var commit_websocket = undefined;
$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://127.0.0.1:8080/codenerix_pos_client/';
    // console.log("Connecting to " + ws_path)
    var socket = new WebSocket(ws_path);
    if (socket) {
        socket.onerror = function(ev) {
            if (typeof(local_uuid_callback) != "undefined"){
                local_uuid_callback(undefined, true);
            }
        }
        socket.onmessage = function(message) {
            socket.close();
            try {
                var data = JSON.parse(message.data);
            } catch (e) {
                var data = null;
            }
            if (typeof(data.uuid) != 'undefined') {
                uuid_websocket = data.uuid;
                key_websocket = data.key;
                commit_websocket = data.commit;
                
                data['csrfmiddlewaretoken'] = $("input[name='csrfmiddlewaretoken']").val();
                $.post('/codenerix_pos/pos_session', data, function(data){
                    if (typeof(local_uuid_callback) != "undefined"){
                        local_uuid_callback(data, false);
                    }
                }).done(function(data){

                }).fail(function(data){
                    console.error("POS GET Local UUID error detected!");
                    console.error(data);
                    alert("POS GET LOCAL UUID ERROR!");
                }).always(function(data){

                });
            } else {
                console.error("I didn't get an UUID, I got: "+data);
            }
        };
    }
});
