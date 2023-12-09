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
from text_to_speech import TextToSpeechModule

MAX_DETECTION_LENGTH = 20
MAX_PREDICTION_LENGTH = 8


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
        self.dynamicDetectionHistory = deque(maxlen=MAX_DETECTION_LENGTH)
        self.dynamicPredictionHistory = deque(maxlen=MAX_PREDICTION_LENGTH)
        self.dynamicLastPredictionTime = time()
        self.dynamicPredictionCooldown = 3.0
        self.dynamicPredictionThreshold = 0.9
        # self.dynamicLastDetectionTime = time()
        # self.dynamicDetectionCooldown = 1 / 15
        self.dynamicPreviousWord = ""

        # Static Prediction Variable
        self.staticPredictionHistory = deque(maxlen=MAX_DETECTION_LENGTH)
        self.staticDetectionThreshold = 0.9999
        self.staticPredictionCooldown = 0.5
        self.staticAppendCooldown = 1.0
        self.staticLastAppendTime = time() + self.staticAppendCooldown
        self.staticLastDetectTime = time() + self.staticPredictionCooldown

        # Word Segmentation
        self.wordSegmentor = WordSegmentationModule()

        # Sentence Generator
        self.sentenceGenerator = SentenceGeneratorModule()
        self.last_raw_output = ""
        self.lastSentenceGeneration = time()
        self.sentenceGenerationCooldown = 7.0
        self.rawOutputProcessFlag = True

        # Text to Speech
        self.ttsModule = TextToSpeechModule()
        self.tts_previouslySaid = []

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

            # Dynamic Sign Prediction
            if self.settings["detection_mode"] == "Dynamic":
                # When mode changed, segment the static word and append to processedRawOutput
                if self.rawOutputProcessFlag:
                    self.settings["processed_raw_output"].append(self.wordSegmentor.split("".join(self.staticPredictionHistory)))
                    self.staticPredictionHistory.clear()
                    self.rawOutputProcessFlag = False
                
                # Dynamic sign prediction
                # if time() > self.dynamicLastDetectionTime + self.dynamicDetectionCooldown:
                detectionResults, frame = self.featureExtractionModule.extractFeatures(
                    frame
                )
                
                # self.dynamicLastDetectionTime = time()
                detectionResults = detectionResults.astype(np.float32)

                # Save history
                self.dynamicDetectionHistory.append(detectionResults)
                if (
                    len(self.dynamicDetectionHistory)
                    == self.dynamicDetectionHistory.maxlen
                    and time() > self.dynamicLastPredictionTime + self.dynamicPredictionCooldown
                ):
                    # Predict word
                    try:
                        predictionInput = np.array(list(self.dynamicDetectionHistory))
                        predLabel, predAccuracy = self.actionRecognitionModule.predict(predictionInput)
                        
                        if predLabel == 'NONE':
                            self.dynamicLastPredictionTime = time() - self.dynamicPredictionCooldown + 0.1
                        
                        elif predLabel == self.dynamicPreviousWord:
                            self.dynamicLastPredictionTime = time() - self.dynamicPredictionCooldown + 0.1
                            
                        # Append if accuracy is above threshold
                        # elif predAccuracy >= self.dynamicPredictionThreshold:
                        elif predAccuracy >= 0.8:
                            # self.dynamicPredictionHistory.append(str(predLabel) + " (" + str(predAccuracy) +  ")")
                            self.settings["processed_raw_output"].append(str(predLabel))
                            self.settings["raw_output"].append(str(predLabel) + " (" + str(predAccuracy) +  ")")
                            self.dynamicPreviousWord = predLabel

                            if predAccuracy > 0.95:
                                self.dynamicLastPredictionTime = time()

                    except ValueError as e:
                        # Numpy bug that sometimes couldnt parse sequences
                        pass

                # Output
                # self.settings["raw_output"] = list(self.dynamicPredictionHistory)

            else:
                # Static sign prediction
                if not self.rawOutputProcessFlag:
                    self.rawOutputProcessFlag = True
                
                # Hand Detection
                (
                    staticDetectionResults,
                    frame,
                ) = self.staticFeatureExtractionModule.extractFeatures(frame)
                staticDetectionResults = staticDetectionResults.astype(np.float32)

                if time() <= self.staticLastDetectTime + self.staticPredictionCooldown:
                    pass
                else:
                    (
                        predIndex,
                        predLabel,
                        predAccuracy,
                    ) = self.staticRecognitionModule.predict(staticDetectionResults)
                    self.staticLastDetectTime = time()

                    if predAccuracy >= self.staticDetectionThreshold:
                        # If predictionHistory is not empty
                        # If predlabel is the same as the last appended label
                        # Check if appendCooldown have passed since the last append
                        if (
                            self.staticPredictionHistory
                            and predLabel == self.staticPredictionHistory[-1]
                            and time()
                            <= self.staticLastAppendTime + self.staticAppendCooldown
                        ):
                            # Do nothing, don't append
                            pass
                        else:
                            self.staticPredictionHistory.append(str(predLabel))
                            self.settings["raw_output"].append(str(predLabel))
                            # Reset the timestamp when a new character is detected
                            self.staticLastAppendTime = time()
                            
            # Output
            # self.settings["raw_output"].append("Hello")
            # self.settings['raw_output'] = list(self.predictionHistory)

            # Update Kivy Label
            self.settings["update_label_func"](
                self.settings["raw_output"], "raw_output_box"
            )

            # Sentence Transformation
            if self.settings["sentence_assembler"]:
                # Sentence Generator
                if (
                    time() <= self.lastSentenceGeneration + self.sentenceGenerationCooldown
                ):
                    pass
                else:
                    if self.settings["detection_mode"] == "Static":
                        self.settings["processed_raw_output"].append(self.wordSegmentor.split("".join(self.staticPredictionHistory)))
                        self.staticPredictionHistory.clear()

                    # Combine the elements of raw_output into a single string
                    current_raw_output = "".join(self.settings["processed_raw_output"])

                    # Check if the content has changed since the last generation
                    if current_raw_output == self.last_raw_output:
                        self.lastSentenceGeneration = time()
                    else:
                        generatedSentence = self.sentenceGenerator.generate(
                            ", ".join(self.settings["processed_raw_output"]).lower()
                        )
                        self.settings["transformed_output"] = generatedSentence
                        # After generate clear data
                        self.settings["processed_raw_output"] = []

                        # Update last_raw_output to the current content
                        self.last_raw_output = current_raw_output
                        self.lastSentenceGeneration = time()

                self.settings["update_label_func"](
                    self.settings["transformed_output"], "transformed_output_box"
                )

            # Translate
            if self.settings["translate"]:
                # print(self.settings["raw_output"], self.settings["transformed_output"])
                translationTarget = ""
                if self.settings["translate_engine"] == "Google":
                    translationTarget = self.settings["translate_target_google"]
                else:
                    translationTarget = self.settings["translate_target_mymemory"]
                self.settings["translate_instance"].setTarget(translationTarget)

                if self.settings["detection_mode"] == "Dynamic":
                    self.settings["raw_output"] = (
                        self.settings["translate_instance"].translate(
                            " ".join(self.settings["raw_output"])
                        )
                    ).split(" ")

                if len((" ".join(self.settings["raw_output"])).strip()) > 0:
                    self.settings["transformed_output"] = self.settings[
                        "translate_instance"
                    ].translate(self.settings["transformed_output"][:5000])

            # Text to speech
            if self.settings["text_to_speech"]:
                translationTarget = ""
                if self.settings["translate_engine"] == "Google":
                    translationTarget = self.settings["translate_target_google"]
                else:
                    translationTarget = self.settings[
                        "translate_instance"
                    ].mymemoryToGoogle(self.settings["translate_target_mymemory"])

                self.settings["translate_instance"].setTarget(translationTarget)

                if (
                    self.ttsModule.engine == "Pyttsx3"
                    and translationTarget
                    in [
                        "en",
                        "en-GB",
                        "en-AU",
                        "en-CA",
                        "en-IN",
                        "en-IE",
                        "en-NZ",
                        "en-SG",
                        "en-ZA",
                        "en-US",
                    ]
                ) or self.ttsModule.engine == "gTTS":
                    if self.ttsModule.engine == "gTTS":
                        self.ttsModule.setLang(translationTarget)

                    # Extract out the words that havent been said
                    splitPos = 0
                    for i, a in enumerate(
                        self.settings["transformed_output"].split(" ")
                    ):
                        if a != self.tts_previouslySaid[i]:
                            splitPos = i
                            break

                    self.ttsModule.textToSpeech(
                        " ".join(self.settings["transformed_output"][splitPos:])
                    )
                    self.tts_previouslySaid = (
                        self.settings["transformed_output"].copy().split(" ")
                    )

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
