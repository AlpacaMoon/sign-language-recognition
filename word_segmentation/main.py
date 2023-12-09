import wordninja as segmenter

class WordSegmentationModule:
    def split(self, characters):
        self.word_array = segmenter.split(characters)
        return ", ".join(self.word_array).lower()
        
<<<<<<< HEAD

if __name__ == "__main__":
    ws = WordSegmentationModule()
    print(ws.split("ILIKEAPPLE"))
=======
if __name__ == "__main__":
    ws = WordSegmentationModule()
    print(ws.split("ILIKEAPPLE"))   
>>>>>>> ce39fe24bdccdac2d6466cbf0b86ccd758cfc674
