import numpy as np
from .utils import *

# Offset and normalize the landmark list
# Returns a 1d numpy array
def preprocess_landmarks(landmark_list):
    landmark_list = np.array(landmark_list, dtype=float)
    origin = landmark_list[0]

    # Offset every point with respect to the first point
    # Convert to 1D-array
    new_landmark_list = (landmark_list - origin).ravel()

    # Get highest absolute value
    largest_value = getAbsLargestVal(new_landmark_list)

    # Normalization
    if largest_value != 0:
        return new_landmark_list / largest_value
    return new_landmark_list


# Offset and normalize a BBOX list (BBOX = Bounding Box, used in face and hand detection)
# Returns a 1d numpy array
def preprocess_bbox(bbox, frameSize):
    bbox = np.array(bbox, dtype=float)
    # Convert 3rd and 4th element into coordinates instead of width/height
    bbox[2] = bbox[0] + bbox[2]
    bbox[3] = bbox[1] + bbox[3]

    # Normalize against frame size
    bbox[0] /= frameSize[0]
    bbox[1] /= frameSize[1]
    bbox[2] /= frameSize[0]
    bbox[3] /= frameSize[1]

    return bbox


# Normalize a center vertex (a list of 2 elements)
# Returns a 1d numpy array
def preprocess_center(center, frameSize):
    center = np.array(center, dtype=float)
    center[0] /= frameSize[0]
    center[1] /= frameSize[1]
    return center


# Preprocess (Offset and normalize) the body's landmark list, bbox and center
def preprocess_body_part(bodyPart, frameSize):
    bodyPart["lmList"] = preprocess_landmarks(bodyPart["lmList"])
    bodyPart["bbox"] = preprocess_bbox(bodyPart["bbox"], frameSize)
    bodyPart["center"] = preprocess_center(bodyPart["center"], frameSize)
    return bodyPart


# Function to generate empty/placeholder data for a hand
# Used when a hand is not detected in frame
def generate_empty_hand(type):
    return {
        "lmList": np.zeros(21 * 3, dtype=int),
        "bbox": np.zeros(4, dtype=float),
        "center": np.zeros(2, dtype=float),
        "type": type,
    }


# Select the best matching face, aka the one with the best score (clarity)
# and closest to the center of the screen
# Since the Neural network will be design to only accept one face
def select_best_matching_face(faces, frameSize):
    if not faces or len(faces) == 0:
        return False
    elif len(faces) == 1:
        return faces[0]

    def difference(a, b):
        return ((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2)

    frameCenter = (frameSize[0] / 2, frameSize[1] / 2)

    best_score = faces[0]
    best_center = faces[0]
    center_diff = difference(faces[0]["center"], frameCenter)

    for each in faces:
        if difference(each["center"], frameCenter) < center_diff:
            best_center = each
        if each["score"][0] > best_score["score"][0]:
            best_score = each

    if best_center["score"][0] > 0.5:
        return best_center
    return best_score


# Flatten everything
def flattenDetectionResult(obj):
    # return np.fromiter(chain.from_iterable([obj['lmList'], obj['bbox'], obj['center']]), float)
    return np.concatenate([obj["lmList"], obj["bbox"], obj["center"]])
