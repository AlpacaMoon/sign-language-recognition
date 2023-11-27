from gtts import gTTS
from playsound import playsound
import os
from threading import Thread


class GttsTextToSpeechModule:
    # Format:
    #   Name: (language_code, top_level_domain)
    #   language_code is language
    #   top_level_domain is the geographical network domain location to use,
    #       default is 'com' (uses local language accent based on current location)
    accents = {
        "Default": ("", "com"),
        "English (Australia)": ("en", "com.au"),
        "English (United Kingdom)": ("en", "co.uk"),
        "English (United States)": ("en", "us"),
        "English (Canada)": ("en", "ca"),
        "English (India)": ("en", "co.in"),
        "English (Ireland)": ("en", "ie"),
        "English (South Africa)": ("en", "co.za"),
        "French (Canada)": ("fr", "ca"),
        "French (France)": ("fr", "fr"),
        "Mandarin (China Mainland)": ("zh-CN", "com"),
        "Mandarin (Taiwan)": ("zh-TW", "com"),
        "Portuguese (Brazil)": ("pt", "com.br"),
        "Portuguese (Portugal)": ("pt", "pt"),
        "Spanish (Mexico)": ("es", "com.mx"),
        "Spanish (Spain)": ("es", "es"),
        "Spanish (United States)": ("es", "us"),
    }

    def __init__(self):
        self.accent = "Default"

    def setAccent(self, accent):
        if accent in GttsTextToSpeechModule.accents.keys():
            self.accent = accent

    def textToSpeech(self, text):
        # Get audio from google server
        tts = gTTS(text, lang=self.lang, tld=self.accent)

        playAudioThread = Thread(target=self.playAudio, args=(tts))
        playAudioThread.start()

    def playAudio(self, tts: gTTS):
        filename = "temptts.mp3"

        abs_filepath = os.path.join(os.path.dirname(__file__), filename)
        tts.save(abs_filepath)
        playsound(abs_filepath)
        os.remove(abs_filepath)


