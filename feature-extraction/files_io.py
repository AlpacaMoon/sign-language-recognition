from constants import ACTION_LABELS_PATH, KEYPOINTS_PATH
import csv
import os
import numpy as np
import re

def readActionLabels():
    action_labels = []
    with open(ACTION_LABELS_PATH) as f:
        csv_reader = csv.reader(f, delimiter=",")
        action_labels = [each[1] for each in csv_reader]
    return action_labels

def readActionMapping():
    action_mapping = {}
    with open(ACTION_LABELS_PATH) as f:
        csv_reader = csv.reader(f, delimiter=",")
        action_mapping = {each[1]: each[0] for each in csv_reader}
        
    return action_mapping


def initActionLabelFolders(action_labels):
    # Create folder/path for each action label
    for action in action_labels:
        if not os.path.exists(os.path.join(KEYPOINTS_PATH, action)):
            os.makedirs(os.path.join(KEYPOINTS_PATH, action))


def saveKeypoints(action, filename, keypoints, replacement_char="_"):
    invalid_chars_pattern = r'[\/:*?"<>|]'
    _action = re.sub(invalid_chars_pattern, replacement_char, action)
    _filename = re.sub(invalid_chars_pattern, replacement_char, filename)
    
    np.save(os.path.join(KEYPOINTS_PATH, _action, _filename), keypoints)
