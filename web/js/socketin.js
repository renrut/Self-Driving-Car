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
			//
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


	onkeydown = onkeyup = function(e)
	{
	    e = e || event; // to deal with IE
	    if(e.type == 'keydown')
	    {
	        console.log(e.keyCode + " " + String.fromCharCode(e.keyCode).toLowerCase())
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
