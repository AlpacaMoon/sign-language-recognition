from .constants import ACTION_LABELS_PATH, KEYPOINTS_PATH
import csv
import os
import numpy as np
import re

def readActionLabels():
    action_labels = []
    with open(ACTION_LABELS_PATH) as f:
        csv_reader = csv.reader(f, delimiter=",")
        action_labels = {each[0]: each[1] for each in csv_reader}
    return action_labels

def readActionMapping():
    action_mapping = {}
    with open(ACTION_LABELS_PATH) as f:
        csv_reader = csv.reader(f, delimiter=",")
        action_mapping = {each[1]: each[0] for each in csv_reader}
        
    return action_mapping

def secureFilename(filename, replacement_char="_"):
    invalid_chars_pattern = r'[\/:*?"<>|]'
    return re.sub(invalid_chars_pattern, replacement_char, filename)

def initActionLabelFolders(action_labels):
    # Create folder/path for each action label
    for i, action in action_labels.items():
        folder_name = f"{i},{secureFilename(action)}"
        if not os.path.exists(os.path.join(KEYPOINTS_PATH, folder_name)):
            os.makedirs(os.path.join(KEYPOINTS_PATH, folder_name))


def saveKeypoints(action, filename, keypoints):
    _action = secureFilename(action)
    _filename = secureFilename(filename)
    
    np.save(os.path.join(KEYPOINTS_PATH, _action, _filename), keypoints)
