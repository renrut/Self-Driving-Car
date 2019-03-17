var socket = new WebSocket("ws://192.168.86.41:8765");


socket.onopen = function(){

var set = new Set(); // You could also use an array

console.log("Conn open...");

	var sendDriveInput = function()
	{
		var throttle = 0;
		var steering = 0;
		if(set.has('w') || set.has("&"))
		{
			throttle += .5;
		}
		if(set.has('s') || set.has("("))
		{
			throttle -= .5;
		}
		if(set.has('a') || set.has("%"))
		{
			steering += .5;
		}
		if(set.has('d') || set.has("'"))
		{
			steering -= .5;
		}
		var send = "drive " + steering.toString() + "," + throttle.toString();
        console.log("Sending " + send);
		socket.send(send);
	}


    var sendRecord = function()
	{
        socket.send("record");
	}

	var sendStop = function()
	{
        socket.send("stop");
	}

    let gamepad = null;

	var loop = function()
	{
	    gamepad = navigator.getGamepads()[0];
        if(gamepad == null)
        {
            return;
        }
        var x = 0;
        var y = 0;
        if(Math.abs(gamepad.axes[2]) > .05) {
            x = gamepad.axes[2] * -1;
        }
        if(gamepad.buttons[7].pressed) {
            y += gamepad.buttons[7].value;
        }
        if(gamepad.buttons[6].pressed) {
            y -= gamepad.buttons[6].value;
        }

        var send = "drive " + x + "," + y;
		socket.send(send);
	}

    var interval = null;
    window.addEventListener("gamepadconnected", function(e) {
      console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
        e.gamepad.index, e.gamepad.id,
        e.gamepad.buttons.length, e.gamepad.axes.length);
        gamepad = e.gamepad;
        document.getElementById("gamepad-prompt").innerText = "Gamepad Connected"
        interval = setInterval(loop, 1000/30)
    });

    window.addEventListener("gamepaddisconnected", function(e) {
      console.log("Gamepad disconnected.");
        document.getElementById("gamepad-prompt").innerText = "Gamepad Disconnected"
        clearInterval(interval)
        gamepad = null
    });

	onkeydown = onkeyup = function(e)
	{
	    e = e || event; // to deal with IE
	    if(e.type == 'keydown')
	    {
	    	set.add(String.fromCharCode(e.keyCode).toLowerCase())
	    }
	    if(e.type == 'keyup')
	    {
			set.delete(String.fromCharCode(e.keyCode).toLowerCase())
	    }
	    sendDriveInput();
	}






	document.getElementById("record-button").onclick = function(e)
	{
	    sendRecord();
	}

	document.getElementById("stop-button").onclick = function(e)
	{
	    sendStop();
	}
}

socket.onclose = function (evt) {
    console.log("Conn closed..." + JSON.stringify(evt));
};

socket.onerror = function (evt) {
    console.log("ERR: " + evt.data);
};
