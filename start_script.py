#Startup script. Just run `python start_script.py`

from web_controller import WebSocketController
from web_server import WebServer
from threading import Thread

threads = []
websocketcontroller = WebSocketController()
webserver = WebServer()
threads.append(Thread(target=websocketcontroller.run))
threads.append(Thread(target=webserver.run))
[thread.start() for thread in threads]