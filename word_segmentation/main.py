import wordninja as segmenter

class WordSegmentationModule:
    def split(self, characters):
        self.word_array = segmenter.split(characters)
        return ", ".join(self.word_array).lower()
        
ws = WordSegmentationModule()
print(ws.split("ILIKEAPPLE"))