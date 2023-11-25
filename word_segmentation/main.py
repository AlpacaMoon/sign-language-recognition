import wordninja as segmenter

class WordSegmentationModule():
      
    def split(self, characters):
        self.word_array = segmenter.split(characters)
        return self
    
    def to_string(self):
        if hasattr(self, 'word_array'):
            return ', '.join(self.word_array)
        else:
            raise ValueError("No word array. Please call split() first.")
    