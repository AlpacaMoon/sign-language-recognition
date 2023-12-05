from deep_translator import GoogleTranslator, MyMemoryTranslator
import json
import os


class TranslationModule:
    # These are the language code conversions from MyMemory to Google
    # Other language codes are the same between MyMemory & Google (except those listed in 'only_in_google' below)
    mymemory_to_google_mapping = {
        "ayr-BO": "ay",
        "ny-MW": "ny",
        "dv-MV": "dv",
        "ht-HT": "ht",
        "ibo-NG": "ig",
        "ig-NG": "ig",
        "ga-IE": "ga",
        "kmr-TR": "ku",
        "ckb-IQ": "ckb",
        "mni-IN": "mni-Mtei",
        "nb-NO": "no",
        "nn-NO": "no",
        "or-IN": "or",
        "ory-IN": "or",
        "gaz-ET": "om",
        "nso-ZA": "nso",
        "sr-Cyrl-RS": "sr",
        "sr-Latn-RS": "sr",
        "snd-PK": "sd",
        "sd-PK": "sd",
        "ta-IN": "ta",
        "ta-LK": "ta",
        "uig-CN": "ug",
        "ug-CN": "ug",
    }

    # These are the language codes that are supported by Google but not by MyMemory
    only_in_google = {
        "co": "corsican",
        "doi": "dogri",
        "fy": "frisian",
        "kri": "krio",
    }


    def __init__(
        self, source="english", target="english", translator="Google", **kwargs
    ):
        self.source = source
        self.target = target

        # Either "Google" or "MyMemory"
        self.translator = translator

        self.lang = {}
        with open(os.path.join(os.path.dirname(__file__), "lang_google.json"), "r") as f:
            self.lang["Google"] = json.load(f)

        with open(os.path.join(os.path.dirname(__file__), "lang_mymemory.json"), "r") as f:
            self.lang["MyMemory"] = json.load(f)

    def setTranslator(self, translator):
        if translator not in ("Google", "MyMemory"):
            return False

        self.translator = translator
        return True

    def getSupportedLanguages(self):
        return self.lang[self.translator]
    
    def getSupportedLanguagesByEngine(self, engineName):
        return self.lang.get(engineName)    # Returns None if engineName not exist

    def setSource(self, sourceCode):
        if sourceCode not in self.getSupportedLanguages().keys():
            raise Exception("Invalid Translation Code!")
        self.source = sourceCode

    def setTarget(self, targetCode):
        if targetCode not in self.getSupportedLanguages().keys():
            raise Exception("Invalid Translation Code!")
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
        if langCode in GoogleTranslator().get_supported_languages().keys():
            return langCode
        
        elif langCode in TranslationModule.mymemory_to_google_mapping.keys():
            return TranslationModule.mymemory_to_google_mapping[langCode]

        # Language cannot be converted to Google code
        return False
