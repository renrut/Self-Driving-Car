import logging
import socketserver
from aiohttp import web
import asyncio
import websockets
from mechanics.camera_controller import CameraController
from mechanics.steering_controller import SteeringController
from mechanics.throttle_controller import ThrottleController

config = open("config/steering.config", "r")
steeringrange = config.readline().split(',')
throttlerange = config.readline().split(',')

steering = SteeringController(int(steeringrange[0]), int(steeringrange[1]))
throttle = ThrottleController(int(throttlerange[0]), int(throttlerange[1]), int(throttlerange[2]))

camera = CameraController()

async def handle_index(request):
    print("Index")
    return web.FileResponse('./web/frontpage.html')


async def handle_resources_js(request):
    name = request.match_info.get('name')
    print("Js:" + name)
    return web.FileResponse('./web/js/' + name)

async def handle_resources_css(request):
    name = request.match_info.get('name')
    print("Css:" + name)
    return web.FileResponse('./web/css/' + name)


async def handle_stream(request):
    print("Stream")
    # try:
    #     output = camera.get_streaming_output()
    #     response = web.StreamResponse()
    #     response.content_type = 'multipart/x-mixed-replace;boundary=ffserver'
    #     while True:
    #         with output.condition:
    #             output.condition.wait()
    #             frame = output.frame
    #         data = frame
    #         response.write(data)
    # except Exception as e:
    #     print("Exception")


async def callback(websocket, path):
    print("callback called")
    try:
        while True:
            datastr = await websocket.recv()
            if datastr.startswith("drive "):
                datastr = datastr.replace("drive ", "")
                data = datastr.split(',')
                turn = float(data[0])
                speed = float(data[1])
                steering.steer(turn)
                throttle.set_throttle(speed)
            elif datastr.startswith("record"):
                print("recording")
            elif datastr.startswith("stop"):
                print("stopping recording")


    except:
        throttle.set_throttle(0)
        steering.steer(0)

try:
    app = web.Application()
    app.add_routes([web.get('/', handle_index),
                    web.get('/js/{name}', handle_resources_js),
                    web.get('/css/{name}', handle_resources_css),
                    web.get('/stream.mjpg', handle_stream)])
    camera.start()
    address = ('', 8000)
    socketserver = websockets.serve(callback, '0.0.0.0', 8765)
    asyncio.get_event_loop().run_until_complete(socketserver)
    print("serving")
    asyncio.get_event_loop().run_until_complete(web.run_app(app))
    print("serving socket")
    asyncio.get_event_loop().run_forever()

finally:
    print("Exiting")
    steering.steer(0)
    throttle.kill_throttle()
    camera.stop()
