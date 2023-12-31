import numpy as np
import cv2
from collections import deque
import copy
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
MAX_PREDICTION_LENGTH = 10

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
        self.sentenceGenerationCooldown = 5.0
        self.rawOutputProcessFlag = False

        # Translation
        self.translate_prev_raw_output = ""
        self.translate_prev_translated_raw_output = ""
        self.translate_prev_transformed_output = ""
        self.translate_prev_translated_transformed_output = ""

        # Text to Speech
        self.ttsModule = TextToSpeechModule()
        self.ttsNextTime = time()
        self.ttsCooldown = 7.5
        self.ttsLastSaid = ""

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

        # Only start processing if:
        #   - The camera returned something, i.e. the camera is on
        #   - The current frame is different from the previously detected frame. 
        #       This is the because the webcam's FPS might fluctuate (Especially under heavy load)
        #       Causing mismatch between video FPS/refresh rate and the webcam's FPS
        if ret and not np.array_equal(rawFrame, self.previousRawFrame):
            self.previousRawFrame = rawFrame

            # Flip so that the user see's mirror image
            frame = cv2.flip(rawFrame, 1)

            # Dynamic Sign Prediction
            if self.settings["detection_mode"] == "Dynamic":

                # Pre-processing when switching from Static mode to Dynamic mode
                #   When mode changed, segment the static word and append to processedRawOutput
                if self.rawOutputProcessFlag:
                    temp = self.wordSegmentor.split("".join(self.staticPredictionHistory))
                    for each in temp:
                        self.settings["processed_raw_output"].append(each)
                    
                    self.settings["raw_output"] = copy.deepcopy(self.settings["processed_raw_output"])
                    self.staticPredictionHistory.clear()
                    self.rawOutputProcessFlag = False
                
                # Feature Extraction
                detectionResults, frame = self.featureExtractionModule.extractFeatures(
                    frame
                )
                detectionResults = detectionResults.astype(np.float32)

                # Save history
                self.dynamicDetectionHistory.append(detectionResults)
                
                # Start Prediction
                if (
                    len(self.dynamicDetectionHistory) == self.dynamicDetectionHistory.maxlen
                    and time() > self.dynamicLastPredictionTime + self.dynamicPredictionCooldown
                ):
                    try:
                        # Predict word
                        predictionInput = np.array(list(self.dynamicDetectionHistory))
                        predLabel, predAccuracy = self.actionRecognitionModule.predict(predictionInput)
                        
                        # Skip detection for 0.1 seconds if detected nothing 
                        #   The 0.1 seconds is to save resources,
                        #   enforce a max 10 predictions per second, 
                        #   else it'll run prediction every loop
                        if predLabel == 'NONE' or predLabel == self.dynamicPreviousWord:
                            self.dynamicLastPredictionTime = time() - self.dynamicPredictionCooldown + 0.1
                            
                        # Append if accuracy is above threshold
                        elif predAccuracy >= self.dynamicPredictionThreshold:
                            # Raw Output
                            self.settings["raw_output"].append(predLabel)
                            
                            # For sentence generation 
                            self.settings["processed_raw_output"].append(predLabel)

                            self.dynamicPreviousWord = predLabel
                            self.dynamicLastPredictionTime = time()

                    except ValueError as e:
                        # Numpy bug that sometimes couldnt parse sequences??
                        pass

            # Static sign prediction
            else:
                # Flag for Switching between Static mode and Dynamic mode
                if not self.rawOutputProcessFlag:
                    self.rawOutputProcessFlag = True
                
                # Hand Detection
                (
                    staticDetectionResults,
                    frame,
                ) = self.staticFeatureExtractionModule.extractFeatures(frame)
                staticDetectionResults = staticDetectionResults.astype(np.float32)

                if time() > self.staticLastDetectTime + self.staticPredictionCooldown:
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

            # Update Final Raw Output
            #   *This may be overwritten later, eg. for translations
            self.settings['final_raw_output'] = " ".join(self.settings['raw_output'])

            # Sentence Transformation
            if self.settings["sentence_assembler"]:
                # Sentence Generator
                if (
                    time() > self.lastSentenceGeneration + self.sentenceGenerationCooldown
                ):
                    current_raw_output = (", ".join(self.settings["processed_raw_output"])).lower()
                    # Check if the content has changed since the last generation
                    if current_raw_output == self.last_raw_output or len(current_raw_output) == 0:
                        self.lastSentenceGeneration = time()
                    else:
                        generatedSentence = self.sentenceGenerator.generate(
                            current_raw_output
                        )
                        self.settings["transformed_output"] = generatedSentence
                        # After generate clear data

                        # Update last_raw_output to the current content
                        self.last_raw_output = current_raw_output
                        self.lastSentenceGeneration = time()

                self.settings['final_transformed_output'] = self.settings['transformed_output']
            
            # Translate
            if self.settings["translate"]:

                # Set target language and target font for translation
                #   *Some languages can only be displayed with their own font
                translationTarget = ""
                fontTarget = ""
                if self.settings["translate_engine"] == "Google":
                    translationTarget = self.settings["translate_target_google"]
                    fontTarget = self.settings['translate_instance'].getFont(translationTarget)
                else:
                    translationTarget = self.settings["translate_target_mymemory"]
                    fontTarget = self.settings['translate_instance'].getFont(
                        self.settings['translate_instance'].mymemory_to_google_mapping.get(translationTarget)
                    )
                self.settings["translate_instance"].setTarget(translationTarget)

                # Only translate raw output if current mode is Dynamic
                if (
                    self.settings['detection_mode'] == 'Dynamic' 
                    and len(self.settings['raw_output']) > 0
                ):
                    # Send translate API request
                    #   Only if the current sentence hasn't been translated before
                    if (
                        self.settings['language_changed']
                        or self.translate_prev_raw_output != self.settings['raw_output'] 
                    ):
                        self.translate_prev_raw_output = self.settings['raw_output']

                        new_raw_output = self.settings['translate_instance'].translate(
                            " ".join(self.settings['raw_output'])
                        )

                        # Override Raw output label
                        self.settings['final_raw_output'] = new_raw_output
                        self.translate_prev_translated_raw_output = new_raw_output
                    
                    # Use previous translation to save resources
                    else:
                        self.settings['final_raw_output'] = self.translate_prev_translated_raw_output
                
                # Translate transformed output no matter dynamic or static mode
                if (
                    len(self.settings['final_transformed_output'].strip()) > 0
                ):
                    # Send translate API request
                    #   Only if the current sentence hasn't been translated before
                    if (
                        self.settings['language_changed']
                        or self.translate_prev_transformed_output != self.settings['transformed_output']
                    ):
                        self.translate_prev_transformed_output = self.settings['final_transformed_output']
                        self.settings['language_changed'] = False

                        new_transformed_output = self.settings['translate_instance'].translate(
                            self.settings['transformed_output']
                        )

                        # Override Raw output label
                        self.settings['final_transformed_output'] = new_transformed_output
                        self.translate_prev_translated_transformed_output = new_transformed_output

                    # Use previous translation to save resources
                    else:
                        self.settings['final_transformed_output'] = self.translate_prev_translated_transformed_output

                # Update font
                if self.settings['detection_mode'] == 'Dynamic':
                    self.settings['update_display_font'](fontTarget, fontTarget)
                else:
                    self.settings['update_display_font'](
                        "fonts/" + self.settings['translate_instance'].font_files['default'], fontTarget
                    )

            # Use default font if translate is disabled
            else:
                self.settings['update_display_font'](
                    "fonts/" + self.settings['translate_instance'].font_files['default'], 
                    "fonts/" + self.settings['translate_instance'].font_files['default']
                )

            # Text-to-speech
            if (
                self.settings["text_to_speech"] 
                and time() > self.ttsNextTime
                and self.settings["sentence_assembler"]
                and len(self.settings['final_transformed_output']) > 0
            ):
                # Periodically check if the sentence was updated or not every 1 second
                if self.ttsLastSaid == self.settings['final_transformed_output'] and not self.settings['language_changed']:
                    self.ttsNextTime = time() + 1.0

                # Perform TTS
                else:
                    # Get language
                    translationTarget = ""
                    if self.settings["translate_engine"] == "Google":
                        translationTarget = self.settings["translate_target_google"]
                    else:
                        translationTarget = self.settings[
                            "translate_instance"
                        ].mymemoryToGoogle(self.settings["translate_target_mymemory"])

                    self.ttsModule.setLang(translationTarget)

                    # Generate Speech
                    self.ttsModule.textToSpeech(
                        self.settings["final_transformed_output"]
                    )

                    # Post-processing
                    self.ttsNextTime = time() + self.ttsCooldown
                    self.ttsLastSaid = self.settings['final_transformed_output']

            # Update Kivy labels
            self.settings["update_label_func"](
                self.settings["final_raw_output"], "raw_output_box"
            )
            self.settings["update_label_func"](
                self.settings["final_transformed_output"], "transformed_output_box"
            )
            
            # Limit the display size of the output
            while len(' '.join(self.settings['processed_raw_output'])) > 70:
                del self.settings['raw_output'][0]
                del self.settings['processed_raw_output'][0]

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