import os

# How many video records / training data each label should have
TRAININGS_PER_LABEL = 200

# How many frames each video record / training data should have
FRAMES_PER_TRAINING = 1

# How many keypoint values does each frame has
KEYPOINTS_PER_FRAME = 240


ACTION_LABELS_PATH = os.path.join('../static-recognition/static-labels.csv')

KEYPOINTS_PATH = os.path.join("../static-recognition/keypoints_data")
