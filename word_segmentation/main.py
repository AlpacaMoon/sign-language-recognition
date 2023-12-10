import wordninja as segmenter

class WordSegmentationModule:
    def split(self, characters):
        self.word_array = segmenter.split(characters)
        temp = []
        # return ", ".join(self.word_array).lower()
        for i in range(len(self.word_array)):
            self.word_array[i] = self.word_array[i].lower()
        return self.word_array

from collections import deque
if __name__ == "__main__":
    ws = WordSegmentationModule()
    print(len(ws.split("Applea")))
    print(ws.split("Applea"))