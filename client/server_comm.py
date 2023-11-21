import asyncio
import websockets
import numpy as np

async def communicate_with_server(frame):
    async with websockets.connect("ws://your-server-ip:8000/ws") as websocket:
        # Example usage: Sending a NumPy array to the server
        # input_frame = np.random.rand(1280, 720).astype(np.float32)
        input_frame_data = frame.tobytes()
        await websocket.send(input_frame_data)

        # Receive the processed frame from the server
        processed_frame_data = await websocket.recv()
        processed_frame = np.frombuffer(processed_frame_data, dtype=np.float32)
        print("Received processed frame:", processed_frame)
        return processed_frame

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(communicate_with_server())
