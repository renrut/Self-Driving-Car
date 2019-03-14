var socket = new WebSocket("ws://192.168.86.41:8766");
var img = document.querySelector('img');



socket.onopen = function()
{
    console.log("Camera conn open...");
}

socket.onmessage = function(message)
{
    if(img == null)
    {
         img = document.querySelector('img');
    }
    // set the base64 string to the src tag of the image
    var objectURL = URL.createObjectURL(message.data);
    img.src = objectURL;
}

socket.onclose = function (evt)
{
    console.log("Conn closed..." + JSON.stringify(evt));
};

socket.onerror = function (evt)
{
    console.log("ERR: " + evt.data);
};
