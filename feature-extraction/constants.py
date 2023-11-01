import os

# How many video records / training data each label should have
TRAININGS_PER_LABEL = 100

# How many frames each video record / training data should have
FRAMES_PER_TRAINING = 15

ACTION_LABELS_PATH = os.path.join('../action-recognition/action-labels.csv')

KEYPOINTS_PATH = os.path.join("../action-recognition/keypoints_data")
