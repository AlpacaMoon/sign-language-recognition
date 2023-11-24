import asyncio
import websockets
import numpy as np
from queue import Queue
from threading import Event
import json

async def send_numpy_array(websocket, data=np.ndarray):
    try:
        data_shape = {'shape': data.shape}
        
        # Send
        await websocket.send(data.tobytes())
        await websocket.send(json.dumps(data_shape))

        # Receive
        response_data = await websocket.recv()
        return response_data

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed by server: {e}")
    except Exception as e:
        print(f"Error during data sending: {e}")

async def websocket_task(uri, in_queue: Queue, out_queue: Queue, stop_flag: Event):
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                if not in_queue.empty():
                    next_data = in_queue.get()
                    response_data = await send_numpy_array(websocket, next_data)
                    out_queue.put(response_data)
                elif stop_flag.is_set():
                    break
                else:
                    await asyncio.sleep(0.1)
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed by server: {e}")
    except Exception as e:
        print(f"Error during connection: {e}")

def start_websocket_task(uri, in_queue: Queue, out_queue: Queue, stop_flag: Event):
    asyncio.run(websocket_task(uri, in_queue, out_queue, stop_flag))