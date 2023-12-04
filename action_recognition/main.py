import os
import keras
import numpy as np
import csv

MODEL_PATH = "models"
MODEL_NAME = "model_v3_5.keras"
ACTION_LABELS_PATH = "action_labels.csv"


class ActionRecognitionModule:
    def __init__(self, **kwargs):
        self.model_path = os.path.join(
            os.path.dirname(__file__), MODEL_PATH, MODEL_NAME
        )

        self.model = keras.models.load_model(self.model_path)

        self.action_labels = []

        with open(os.path.join(os.path.dirname(__file__), ACTION_LABELS_PATH), "r") as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                self.action_labels.append(row[1])

    # Accepts an input numpy array of shape (20, 240)
    def predict(self, inputValue):
        predResult = self.model.predict(
            np.expand_dims(inputValue, axis=0),
            verbose=0,
            workers=4,
            use_multiprocessing=True,
        )
        predIndex = np.argmax(predResult)
        predLabel = self.action_labels[predIndex]
        return predIndex, predLabel
