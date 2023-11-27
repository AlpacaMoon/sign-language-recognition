from queue import Queue
from threading import Thread, Event
import numpy as np
from time import sleep, time
import traceback

from client.server_comm import start_websocket_task

if __name__ == "__main__":

    # Server Communication API Link
    action_translation_uri = "ws://52.221.215.40:80/ws"

    # Shared Queue with the server communication thread
    server_comm_queue = Queue()
    result_queue = Queue()
    stop_flag = Event()

    # Start server communication thread
    server_comm_thread = Thread(target=start_websocket_task, args=(action_translation_uri, server_comm_queue, result_queue, stop_flag))
    server_comm_thread.start()


    testData = np.random.rand(1280, 720, 3)
    testData = testData.astype(np.float32)
    server_comm_queue.put(testData)
    t1 = time()
    print("Shape: ", testData.shape)
    print("Sum: ", np.sum(testData))
    print("Avg: ", np.average(testData))
    print("===============")

    try:
        while True:
            if not result_queue.empty():
                t2 = time()
                output = result_queue.get()
                print(output)
                print(f"Time taken: {t2-t1} seconds")
                break
            else:
                sleep(0.1)
    except KeyboardInterrupt:
        print("Finished")
    except Exception as e:
        print(e)
        traceback.print_exc()
    finally:
        stop_flag.set()