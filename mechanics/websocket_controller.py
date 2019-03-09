#!/usr/bin/env python

import asyncio
import websockets

class websocket_controller:
    def __init__(self):
        self.server = None

    def start_connection(self, callback):
        self.server = websockets.serve(callback, '0.0.0.0', 8765)
        print("in start_connection")
        asyncio.get_event_loop().run_until_complete(self.server)

    def event_loop(self):
        asyncio.get_event_loop().run_forever()
