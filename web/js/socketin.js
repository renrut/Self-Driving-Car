
var socket = new WebSocket("ws://192.168.86.41:8765");

socket.onopen = function(){
    console.log("Conn open...");
    document.onkeypress = function (e) {
        e = e || window.event;
        var code = String.fromCharCode(e.keyCode);
        console.log("sending:" + code)
        socket.send(code);
    };
}

socket.onclose = function (evt) {
    console.log("Conn closed..." + JSON.stringify(evt));
};

socket.onerror = function (evt) {
    console.log("ERR: " + evt.data);
};
