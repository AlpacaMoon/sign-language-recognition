from deep_translator import GoogleTranslator, MyMemoryTranslator
import json
import os

class TranslationModule:
    # These are the language code conversions from MyMemory to Google
    # Other language codes are the same between MyMemory & Google (except those listed in 'only_in_google' below)
    mymemory_to_google_mapping = {
        "zh-CN": "zh-CN",
        "zh-TW": "zh-TW",
        "en-GB": "en",
        "fil-PH": "tl",
        "fr-FR": "fr",
        "de-DE": "de",
        "id-ID": "id",
        "it-IT": "it",
        "ja-JP": "ja",
        "ko-KR": "ko",
        "ms-MY": "ms",
        "pl-PL": "pl",
        "pt-PT": "pt",
        "ru-RU": "ru",
        "es-ES": "es",
        "sv-SE": "sv",
        "th-TH": "th",
        "vi-VN": "vi",
    }

    # Font Files
    font_files = {
        "zh-CN": "NotoSansSC-Bold.ttf",
        "zh-TW": "NotoSansTC-Bold.ttf",
        "ja": "NotoSerifJP-Bold.otf",
        "ko": "NotoSansKR-Bold.ttf",
        "th": "NotoSansThai-Bold.ttf",
        "default": "NotoSans-Bold.ttf",
    }

    def __init__(
        self, source="english", target="english", translator="Google", **kwargs
    ):
        self.source = source
        self.target = target

        # Either "Google" or "MyMemory"
        self.translator = translator

        self.lang = {}
        with open(
            os.path.join(os.path.dirname(__file__), "lang_google.json"), "r"
        ) as f:
            self.lang["Google"] = json.load(f)

        with open(
            os.path.join(os.path.dirname(__file__), "lang_mymemory.json"), "r"
        ) as f:
            self.lang["MyMemory"] = json.load(f)

    def setTranslator(self, translator):
        if translator not in ("Google", "MyMemory"):
            return False

        self.translator = translator
        return True

    def getSupportedLanguages(self):
        return self.lang[self.translator]

    def getSupportedLanguagesByEngine(self, engineName):
        return self.lang.get(engineName)  # Returns None if engineName not exist

    def setSource(self, sourceCode):
        # if sourceCode not in self.getSupportedLanguages().keys():
        #     raise Exception("Invalid Translation Code!")
        self.source = sourceCode

    def setTarget(self, targetCode):
        # if targetCode not in self.getSupportedLanguages().keys():
        #     raise Exception("Invalid Translation Code!")
        self.target = targetCode

    def translate(self, text):
        if self.translator == "Google":
            return GoogleTranslator(source=self.source, target=self.target).translate(
                text=text
            )
        elif self.translator == "MyMemory":
            return MyMemoryTranslator(source=self.source, target=self.target).translate(
                text=text
            )
        else:
            raise Exception("Invalid Translation Type!")

    def mymemoryToGoogle(self, langCode):
        return TranslationModule.mymemory_to_google_mapping.get(langCode)

    # Accepts langCode in Google
    def getFont(self, langCode):
        if langCode in TranslationModule.font_files.keys():
            return "fonts/" + str(TranslationModule.font_files.get(langCode))

        return "fonts/" + str(TranslationModule.font_files.get('default'))
