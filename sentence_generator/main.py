from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import time
import torch
import os

class SentenceGeneratorModule:
    hugginFaceModelId = "EngLip/flan-t5-sentence-generator"
    localModelPath = "./sentence_generator/model"

    def __init__(self, device="cuda:0" if torch.cuda.is_available() else "cpu"):
        if not os.path.exists(self.localModelPath):
            self.download_model()
        else:
            # Load the saved tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.localModelPath)
            # Load the saved model
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.localModelPath)

        self.device = device
        self.model.to(self.device)

    def generate(self, input_text):
        # Tokenize the input text
        inputs = self.tokenizer(
            input_text, return_tensors="pt", max_length=512, truncation=True
        )

        # Move inputs to GPU if available
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        # Generate output from the model
        outputs = self.model.generate(
            **inputs, max_length=50, num_beams=5, no_repeat_ngram_size=2
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def download_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.hugginFaceModelId)
        self.tokenizer.save_pretrained(self.localModelPath)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.hugginFaceModelId)
        self.model.save_pretrained(self.localModelPath)