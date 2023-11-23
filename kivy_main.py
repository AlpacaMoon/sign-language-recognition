from queue import Queue
from threading import Thread
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import numpy as np
import cv2

from action_feature_extraction import FeatureExtractionModule
from client.server_comm import start_websocket_task




kv_script_main = """
Screen:
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: "vertical"
                   
                    MDTopAppBar:
                        title: "Sign Language Translation App"
                        right_action_items: [["cog", lambda x: nav_drawer.set_state("open")]]
                        elevation: 8
                   
                    # Main Area
                    FloatLayout:


                        # Left Panel for video display
                        BoxLayout:
                            size_hint: 0.75, 1
                            pos_hint: {'x': 0}


                            FloatLayout:
                                BoxLayout:
                                    size_hint: 1, 0.75
                                    pos_hint: {'y': 0.25}


                                    Button:
                                        text:"fas"


                                BoxLayout:
                                    size_hint: 1, 0.25
                                    pos_hint: {'y': 0}


                                    Button:
                                        text: "fnasb"
                                   
                        # Right Panel for output/translation display
                        BoxLayout:
                            size_hint: 0.25, 1
                            pos_hint: {'x': 0.75}
                            padding: 5
                           
                            Button:
                                text: "fbadsafa"




        MDNavigationDrawer:
            id: nav_drawer
            anchor: 'right'        
"""


class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.playing = False


        # FPS here implies the video's refresh rate, but not the webcam's actual FPS
        self.fps = fps


        self.previousRawFrame = np.zeros(1)


        self.featureExtractionModule = FeatureExtractionModule()
        self.start()


    def start(self):
        self.playing = True
        self.schedule = Clock.schedule_interval(self.update, 1.0 / self.fps)


    def stop(self):
        self.playing = False
        self.schedule.cancel()


    def update(self, dt):
        ret, rawFrame = self.capture.read()


        # Only start processing if the current frame has been updated
        # This is the because the webcam's FPS might fluctuate (Especially under heavy load)
        # Causing mismatch between video FPS/refresh rate and the webcam's FPS
        if ret and not np.array_equal(rawFrame, self.previousRawFrame):
            self.previousRawFrame = rawFrame


            # Flip so that the user see's mirror image
            flippedFrame = cv2.flip(rawFrame, 1)
           
            # Extract Features
            detectionResults, frame = self.featureExtractionModule.extractFeatures(flippedFrame)


            # Flip vertically because of how image texture is displayed
            frame = cv2.flip(frame, 0)


            # Flatten to 1D array (np.flatten is slower than reshape)
            frameLen = frame.shape[0] * frame.shape[1] * frame.shape[2]
            buf = frame.reshape(frameLen)


            # Update texture
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture


class MainApp(MDApp):
    def build(self):
        # Webcam
        # self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # self.my_camera = KivyCamera(capture=self.capture, fps=30)

        # UI Init
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "600"

        # Window
        Window.maximize()

        screen = Builder.load_string(kv_script_main)


        # screen.ids.m_r1c1.add_widget(self.my_camera)
        return screen



if __name__ == "__main__":

    # Server Communication API Link
    action_translation_uri = "ws://your-server-ip:8000/ws"

    # Shared Queue with the server communication thread
    server_comm_queue = Queue()

    # Start server communication thread
    server_comm_thread = Thread(target=start_websocket_task, args=(action_translation_uri, server_comm_queue))
    server_comm_thread.start()

    MainApp().run()
    
    
