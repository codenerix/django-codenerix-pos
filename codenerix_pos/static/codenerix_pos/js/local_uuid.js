$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://127.0.0.1:8080/codenerix_pos_client/';
    // console.log("Connecting to " + ws_path)
    var socket = new WebSocket(ws_path);
    if (socket) {
        socket.onmessage = function(message) {
            socket.close();
            try {
                var data = JSON.parse(message.data);
            } catch (e) {
                var data = null;
            }
            if (typeof(data.uuid) != 'undefined') {
                data['csrfmiddlewaretoken'] = $("input[name='csrfmiddlewaretoken']").val();
                $.post('/codenerix_pos/pos_session', data, function(data){
                    if (data['msg'] != 'OK'){
                        console.log(data['txt']);
                    }
                }).done(function(data){

                }).fail(function(data){
                    alert(data);
                }).always(function(data){

                });
            } else {
                console.error("I didn't get an UUID, I got: "+data);
            }
        };
    }
});
