import asyncio
import websockets
import numpy as np
from queue import Queue
import json

async def send_numpy_array(websocket, data=np.ndarray):
    try:
        data_shape = {'shape': data.shape}
        
        # Send
        await websocket.send(data.tobytes())
        await websocket.send(json.dump(data_shape))

        # Receive
        response_data = await websocket.recv()

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed by server: {e}")
    except Exception as e:
        print(f"Error during data sending: {e}")

async def websocket_task(uri, queue):
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                if not queue.empty():
                    next_data = queue.get()
                    await send_numpy_array(websocket, next_data)
                else:
                    await asyncio.sleep(0.1)
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed by server: {e}")
    except Exception as e:
        print(f"Error during connection: {e}")

def start_websocket_task(uri, queue):
    asyncio.run(websocket_task(uri, queue))