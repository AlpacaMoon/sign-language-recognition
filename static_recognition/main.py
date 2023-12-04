import os
import keras
import numpy as np
import csv

MODEL_PATH = "models"
MODEL_NAME = "static_model.h5"
STATIC_LABELS_PATH = "static_labels.csv"

class StaticRecognitionModule():
    def __init__(self, **kwargs):
        self.model_path = os.path.join(os.path.dirname(__file__), MODEL_PATH, MODEL_NAME)

        self.model = keras.models.load_model(self.model_path)

        self.static_labels = []

        with open(os.path.join(os.path.dirname(__file__), STATIC_LABELS_PATH), 'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                self.static_labels.append(row[1])

    # Accepts an input numpy array of shape (1, 138)
    def predict(self, inputValue):
        predResult = self.model.predict(
            np.expand_dims(inputValue, axis=0), verbose=0, workers=4, use_multiprocessing=True
        )
        predIndex = np.argmax(predResult)
        predLabel = self.static_labels[predIndex]
        predAccuracy = predResult[np.argmax(predResult)]
        return predIndex, predLabel, predAccuracy
        