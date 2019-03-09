var socket = new WebSocket("ws://192.168.86.41:8765");


socket.onopen = function(){

var set = new Set(); // You could also use an array

console.log("Conn open...");

	var sendInput = function()
	{
		var throttle = 0;
		var steering = 0;
		if(set.has('w'))
		{
			throttle += .5;
		}
		if(set.has('s'))
		{
			throttle -= .5;
		}
		if(set.has('a'))
		{
			steering += .5;
		}
		if(set.has('d'))
		{
			steering -= .5;
		}
		var send = steering.toString() + "," + throttle.toString();
        console.log("Sending" + send);
		socket.send(send);
	}

	onkeydown = onkeyup = function(e){
	    e = e || event; // to deal with IE
	    if(e.type == 'keydown')
	    {
	    	set.add(String.fromCharCode(e.keyCode).toLowerCase())
	    }
	    if(e.type == 'keyup')
	    {
			set.delete(String.fromCharCode(e.keyCode).toLowerCase())
	    }
	    sendInput();
	}
}

socket.onclose = function (evt) {
    console.log("Conn closed..." + JSON.stringify(evt));
};

socket.onerror = function (evt) {
    console.log("ERR: " + evt.data);
};
