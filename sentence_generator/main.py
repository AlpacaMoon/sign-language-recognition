from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

class SentenceGenerator:
    hugginFaceModelId = "EngLip/flan-t5-sentence-generator"
    localModelPath = "./sentence_generator/model"
    tokenizer = AutoTokenizer
    model = AutoModelForSeq2SeqLM
    
    def __init__(self):
        self.download_model()
        # # Load the saved tokenizer
        # self.tokenizer = AutoTokenizer.from_pretrained(self.localModelPath)
        # # Load the saved model
        # self.model = AutoModelForSeq2SeqLM.from_pretrained(self.localModelPath)

    def generate(self, input_text):
        # Tokenize the input text
        inputs = self.tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
        # Generate output from the model
        outputs = self.model.generate(**inputs, max_length=50, num_beams=5, no_repeat_ngram_size=2)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    def download_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.hugginFaceModelId)
        # self.tokenizer.save_pretrained(self.localModelPath)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.hugginFaceModelId)
        # self.model.save_pretrained(self.localModelPath)