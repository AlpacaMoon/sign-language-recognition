import os

# How many video records / training data each label should have
TRAININGS_PER_LABEL = 100

# How many frames each video record / training data should have
FRAMES_PER_TRAINING = 20

# How many keypoint values does each frame has
KEYPOINTS_PER_FRAME = 240


ACTION_LABELS_PATH = os.path.join('../action_recognition/action_labels.csv')

KEYPOINTS_PATH = os.path.join("../action_recognition/keypoints_data")
# KEYPOINTS_PATH = os.path.join("../action_recognition/new_keypoints_data")
