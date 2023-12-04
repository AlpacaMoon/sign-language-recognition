import numpy as np
import cv2
from collections import deque
from time import time

from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from action_feature_extraction import FeatureExtractionModule
from action_recognition import ActionRecognitionModule
from static_feature_extraction import StaticFeatureExtractionModule
from static_recognition import StaticRecognitionModule
from word_segmentation import WordSegmentationModule
from sentence_generator import SentenceGeneratorModule

MAX_DETECTION_LENGTH = 20
MAX_PREDICTION_LENGTH = 20


class KivyCamera(Image):
    def __init__(self, fps, translation_settings, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = None

        self.settings = translation_settings

        self.playing = False
        self.opacity = 0

        # FPS here implies the video's refresh rate, but not the webcam's actual FPS
        self.fps = fps

        self.previousRawFrame = np.zeros(1)

        self.featureExtractionModule = FeatureExtractionModule()
        self.actionRecognitionModule = ActionRecognitionModule()
        self.staticFeatureExtractionModule = StaticFeatureExtractionModule()
        self.staticRecognitionModule = StaticRecognitionModule()

        # Dynamic Prediction Variables
        self.detectionHistory = deque(maxlen=MAX_DETECTION_LENGTH)
        self.predictionHistory = deque(maxlen=MAX_PREDICTION_LENGTH)
        self.lastPredictionTime = time()
        self.predictionCooldown = 1.0
        self.detectionThreshold = 1.0
        
        # Static Prediction Variable
        self.staticPredictionHistory = deque(maxlen=MAX_DETECTION_LENGTH)
        self.staticDetectionThreshold = 0.999    
        self.staticPredictionCooldown = 0.5
        self.staticAppendCooldown = 1.0
        self.staticLastAppendTime = time() + self.staticAppendCooldown
        self.staticLastDetectTime = time() + self.predictionCooldown
        
        # Word Segmentation
        self.wordSegmentor = WordSegmentationModule()
        
        # Sentence Generator
        self.sentenceGenerator = SentenceGeneratorModule()

    def start(self):
        if not self.playing:
            self.playing = True
            self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.schedule = Clock.schedule_interval(self.update, 1.0 / self.fps)
            self.opacity = 1

    def stop(self):
        if self.playing:
            self.schedule.cancel()
            self.capture.release()
            self.playing = False
            self.opacity = 0

    def update(self, dt):
        ret, rawFrame = self.capture.read()

        # Only start processing if the current frame has been updated
        # This is the because the webcam's FPS might fluctuate (Especially under heavy load)
        # Causing mismatch between video FPS/refresh rate and the webcam's FPS
        if ret and not np.array_equal(rawFrame, self.previousRawFrame):
            self.previousRawFrame = rawFrame

            # Flip so that the user see's mirror image
            frame = cv2.flip(rawFrame, 1)

            # Extract Features
            if self.settings["detection_mode"] == "Dynamic":
                if self.staticPredictionHistory:
                    # When mode change segment the static character? 
                    self.settings["raw_output"].append(self.wordSegmentor.split(self.staticPredictionHistory))
                    self.staticPredictionHistory.clear()
                
                # Dynamic sign prediction
                detectionResults, frame = self.featureExtractionModule.extractFeatures(
                    frame
                )

                # Save history
                self.detectionHistory.append(detectionResults)
                if len(self.detectionHistory) == self.detectionHistory.maxlen:
                    # Predict word
                    if self.settings["prediction_mode"] == "Local":
                        # Run model.predict(...)
                        predIndex, predLabel = self.actionRecognitionModule.predict(
                            np.array(self.detectionHistory)
                        )
                        self.predictionHistory.append(predLabel)
                    else:
                        # Send result to remote server
                        predictionResults = "Apple"
                        ...

            else:
                # Static sign prediction
                # Hand Detection
                detectionResults, frame = self.staticFeatureExtractionModule.extractFeatures(frame)

                if time() <= self.staticLastDetectTime + self.staticPredictionCooldown:
                    pass
                else:
                    predIndex, predLabel, predAccuracy = self.staticRecognitionModule.predict(detectionResults)          
                    
                    if predAccuracy >= self.staticDetectionThreshold:            
                        # If predictionHistory is not empty
                        # If predlabel is the same as the last appended label
                        # Check if appendCooldown have passed since the last append
                        if self.staticPredictionHistory and predLabel == self.staticPredictionHistory[-1] and time() <= self.staticLastAppendTime + self.staticAppendCooldown:
                            # Do nothing, don't append
                            pass
                        else:
                            self.staticPredictionHistory.append(predLabel)
                            # Reset the timestamp when a new character is detected
                            self.staticLastAppendTime = time()              

            # Output
            # self.settings["raw_output"].append("Hello")
            self.settings['raw_output'] = list(self.predictionHistory)

            if len(self.settings["raw_output"]) > self.settings["max_output_len"]:
                del self.settings["raw_output"][0]

            self.settings["update_label_func"](
                self.settings["raw_output"], "raw_output_box"
            )

            # Sentence Transformation
            if self.settings["sentence_assembler"]:
                # Sentence Generator
                self.settings["transformed_output"].append(self.sentenceGenerator.generate(", ".join(self.settings["raw_output"])))

                if (
                    len(self.settings["transformed_output"])
                    > self.settings["max_output_len"]
                ):
                    del self.settings["transformed_output"][0]

                self.settings["update_label_func"](
                    self.settings["transformed_output"], "transformed_output_box"
                )

            # Text to speech
            if self.settings["text_to_speech"]:
                ...

            # Show FPS
            if self.settings["show_fps"]:
                ...

            # Translate
            if self.settings["translate"]:
                ...

            # Flip vertically because of how image texture is displayed
            frame = cv2.flip(frame, 0)

            # Flatten to 1D array (np.flatten is slower than reshape)
            frameLen = frame.shape[0] * frame.shape[1] * frame.shape[2]
            buf = frame.reshape(frameLen)

            # Update texture
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt="bgr"
            )
            image_texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
            self.texture = image_texture
