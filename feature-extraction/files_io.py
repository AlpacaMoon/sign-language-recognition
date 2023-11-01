from constants import ACTION_LABELS_PATH, KEYPOINTS_PATH
import csv
import os

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