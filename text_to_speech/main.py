from gtts import gTTS
from playsound import playsound
import pyttsx3
import os
from threading import Thread
import json


class isTTS:
    def textToSpeech(self, text):
        return

    def getSupportedLanguages(self) -> dict:
        if hasattr(self, "supportedLanguages"):
            return self.supportedLanguages
        return None


class GttsModule(isTTS):
    def __init__(self):
        with open(
            os.path.join(os.path.dirname(__file__), "tts_lang_google.json"), "r"
        ) as f:
            self.supportedLanguages = json.load(f)

    def textToSpeech(self, text):
        # Get audio from google server
        tts = gTTS(text, lang=self.lang, tld='com')

        playAudioThread = Thread(target=self.playAudio, args=(tts))
        playAudioThread.start()

    def playAudio(self, tts: gTTS):
        filename = "temp_tts.mp3"

        abs_filepath = os.path.join(os.path.dirname(__file__), filename)
        tts.save(abs_filepath)
        playsound(abs_filepath)
        os.remove(abs_filepath)


class Pyttsx3Module(isTTS):
    class PlayAudioThreader(Thread):
        def __init__(self, *args, **kwargs):
            Thread.__init__(self, *args, **kwargs)
            self.daemon = True
            self.start()

        def run(self):
            tts_engine = pyttsx3.init()
            tts_engine.say(self._args)
            tts_engine.runAndWait()

    def __init__(self, **kwargs):
        self.supportedLanguages = {
            "en": "english",
        }

    def textToSpeech(self, text):
        return Pyttsx3Module.PlayAudioThreader(args=text)


class TextToSpeechModule():
    def __init__(self, engine="gTTS", **kwargs):
        self.engine = engine
        self.engineMappings = {
            "gTTS": GttsModule(),
            "Pyttsx3": Pyttsx3Module(),
        }
        self.lang = "en"

    def setLang(self, langCode):
        if langCode in self.getEngine().getSupportedLanguages().keys():
            self.getEngine().lang = langCode
            return True
        
        # Language not Supported
        return False

    def textToSpeech(self, text):
        return self.getEngine().textToSpeech(text)

    def switchEngine(self, engineName):
        temp = self.engineMappings.get(engineName)
        if not temp:
            raise Exception(f"Invalid Text-to-Speech engine name: {engineName}")

        self.engine = engineName
        return True

    def getEngine(self) -> isTTS:
        return self.engineMappings[self.engine]
