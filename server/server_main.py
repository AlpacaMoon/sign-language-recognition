from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import numpy as np
from starlette.middleware.cors import CORSMiddleware
import json
import logging

app = FastAPI()

# Allow requests from all origins during development; adjust as needed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("server.log")
    ]
)

# WebSocket route for handling communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_bytes()
            data_shape_json = json.loads(await websocket.receive_text())

            data_shape = tuple(data_shape_json['shape'])
            frame = np.frombuffer(data, dtype=np.float32).reshape(data_shape)

            # Perform processing using your module
            result = process_frame(frame)

            # Send the processed frame back to the client
            await websocket.send_text(result)

    except WebSocketDisconnect:
        logging.info(f"WebSocket client disconnected. Closing connection. ")
        
    except Exception as e:
        logging.error(f"Error in WebSocket communication: {str(e)}")
        await websocket.close(code=1011)    # Internal Error

# Perform server-side processing, i.e. sign prediction
def process_frame(frame=np.ndarray):
    sum = np.sum(frame)
    avg = np.average(frame)
    return f'The sum is {sum} and the average is {avg}. The shape is {frame.shape}.'
