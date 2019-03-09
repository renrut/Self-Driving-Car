
var socket = new WebSocket("ws://192.168.86.41:8765");

socket.onopen = function(){
    console.log("Conn open...");
    document.onkeypress = function (e) {
        e = e || window.event;
        var code = String.fromCharCode(e.keyCode);
        if e == 'w' {
            socket.send("0.0,0.5")
        }
        else if e == 'a' {
            socket.send("0.75,0.0")
        }
        else if e == 's' {
            socket.send("0.0,-0.2")
        }
        else if e == 'd' {
            socket.send("-0.75,0.0")
        }
    };
}

socket.onclose = function (evt) {
    console.log("Conn closed..." + JSON.stringify(evt));
};

socket.onerror = function (evt) {
    console.log("ERR: " + evt.data);
};
