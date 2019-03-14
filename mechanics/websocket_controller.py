#!/usr/bin/env python

import asyncio
import websockets

class websocket_controller:
    def __init__(self, port=8765):
        self.port = port
        self.server = None

    def start_connection(self, callback):
        self.server = websockets.serve(callback, '0.0.0.0', self.port)
        print("in start_connection")
        asyncio.get_event_loop().run_until_complete(self.server)

    def event_loop(self):
        asyncio.get_event_loop().run_forever()
