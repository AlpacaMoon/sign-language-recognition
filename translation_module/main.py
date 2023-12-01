from deep_translator import GoogleTranslator, MyMemoryTranslator


class TranslationModule:

    # Language title Mappings from MyMemory --> Google
    #   Used in situations such as using gTTS for Text-to-speech while using MyMemory for translation
    #   This is because MyMemory and Google uses different language/code names
    mymemory_to_google_mapping = {
        'central aymara': 'aymara',
        'nyanja': 'chichewa',
        'maldivian': 'dhivehi',
        'chinese simplified': 'chinese (simplified)',
        'chinese traditional': 'chinese (traditional)',
        'haitian creole french': 'haitian creole',
        'igbo ibo': 'igbo',
        'igbo ig': 'igbo',
        'irish gaelic': 'irish',
        'northern kurdish': 'kurdish (kurmanji)',
        'kurdish sorani': 'kurdish (sorani)',
        'manipuri': 'meiteilon (manipuri)',
        'norwegian bokmål': 'norwegian',
        'norwegian nynorsk': 'norwegian',
        'odia': 'odia (oriya)',
        'oriya': 'odia (oriya)',
        'west central oromo': 'oromo',
        'sesotho': 'sepedi',
        'serbian cyrillic': 'serbian',
        'serbian latin': 'serbian',
        'sindhi snd': 'sindhi',
        'sindhi sd': 'sindhi',
        'tamil india': 'tamil',
        'tamil sri lanka': 'tamil',
        'uyghur uig': 'uyghur',
        'uyghur ug': 'uyghur'
    }


    def __init__(
        self, source="english", target="english", translator="Google", **kwargs
    ):
        self.source = source
        self.target = target

        # Either "Google" or "MyMemory"
        self.translator = translator

    def setTranslator(self, translator):
        self.translator = translator

    def getSupportedLanguages(self):
        return self.translator.get_supported_languages(as_dict=True)

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

    def mapLanguageToGoogle(self, lang):
        if lang in GoogleTranslator().get_supported_languages().keys():
            return lang
        
        temp = TranslationModule.mymemory_to_google_mapping.get(lang)
        if temp is not None:
            return temp
        
        return False
