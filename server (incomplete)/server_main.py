from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import numpy as np
from starlette.middleware.cors import CORSMiddleware
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

logger = logging.getLogger(__name__)

# WebSocket route for handling communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_bytes()
            frame = np.frombuffer(data, dtype=np.float32).reshape((1280, 720))

            # Perform processing using your module
            processed_frame = process_frame(frame)

            # Serialize the processed frame
            processed_frame_data = processed_frame.tobytes()

            # Send the processed frame back to the client
            await websocket.send_bytes(processed_frame_data)
    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected. Closing connection. ")
        await websocket.close()
    except Exception as e:
        logger.exception(f"Error in WebSocket communication: {str(e)}")
        await websocket.close(code=1011)    # Internal Error

# Perform server-side processing, i.e. sign prediction
def process_frame(frame):
    # ...
    return frame
