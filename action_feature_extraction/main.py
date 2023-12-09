import numpy as np
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.PoseModule import PoseDetector
from concurrent.futures import ThreadPoolExecutor

from .cvzone_preprocess import *

# NEW
# from itertools import chain

# class FeatureExtractionModule():
#     def __init__(self, **kwargs):
#         # Detectors
#         self.handDetector = HandDetector(detectionCon=0.5, maxHands=2)
#         self.faceDetector = FaceDetector(minDetectionCon=0.5)
#         self.poseDetector = PoseDetector(detectionCon=0.5)

#     def detectHands(self, handDetector, frame, frameSize, draw):
#         results = [0, 0]
#         tempResults = []
#         # Hand Detection
#         if draw:
#             tempResults, frame = handDetector.findHands(frame, draw=draw, flipType=False)
#         else:
#             tempResults = handDetector.findHands(frame, draw=draw, flipType=False)

#         if not tempResults:
#             results = [self.generate_empty_hand("Left"), self.generate_empty_hand("Right")]
#         elif len(tempResults) == 1:
#             if tempResults[0]["type"] == "Left":
#                 results = [self.preprocess_body_part(tempResults[0], frameSize), self.generate_empty_hand("Right")]
#             else:
#                 results = [self.generate_empty_hand("Left"), self.preprocess_body_part(tempResults[0], frameSize)]
#         else:
#             if tempResults[0]['type'] == 'Right' and tempResults[1]['type'] == 'Left':
#                 results[0] = tempResults[1]
#                 results[1] = tempResults[0]
#             elif tempResults[0]['type'] == 'Left' and tempResults[1]['type'] == 'Right':
#                 results[0] = tempResults[0]
#                 results[1] = tempResults[1]

#             # If both detected hands are both left or both right
#             elif tempResults[0]['center'][0] > tempResults[1]['center'][0]:
#                 results[0] = tempResults[1]
#                 results[1] = tempResults[0]
#             else:
#                 results[0] = tempResults[0]
#                 results[1] = tempResults[1]

#             results[0] = self.preprocess_body_part(results[0], frameSize)
#             results[1] = self.preprocess_body_part(results[1], frameSize)

#         return results

#     # Pose Detection
#     # **We only use the first 23 out of the total 33 landmark points
#     #   as those represent the lower half body and are irrelevant to sign language interpretation
#     def detectPose(self, poseDetector, frame, frameSize, draw):
#         frame = poseDetector.findPose(frame, draw=draw)
#         if poseDetector.results.pose_landmarks:
#             results = np.array([[i.x, i.y, i.z, i.visibility] for i in poseDetector.results.pose_landmarks.landmark[:23]])
#             return results.ravel()

#         # frame = poseDetector.findPose(frame, draw=draw)
#         # results, _ = poseDetector.findPosition(frame, bboxWithHands=False)
#         # print('---------------')
#         # print('e1', np.array(results)[:, -1])
#         # if results:
#         #     return np.array(results).flatten()
#         #     # return self.preprocess_landmarks(results[:23], frameSize)
#         # print('e2', results)
#         return np.zeros(92, dtype=float)
        

#     # Face Detection
#     def detectFace(self, faceDetector, frame, frameSize, draw):
#         frame, results = faceDetector.findFaces(frame, draw=draw)
#         if results:
#             results = self.select_best_matching_face(results, frameSize)
#             results["bbox"] = self.preprocess_bbox(results["bbox"], frameSize)
#             results["center"] = self.preprocess_center(results["center"], frameSize)
#             return results

#         return {
#             "bbox": np.zeros(4, dtype=float),
#             "center": np.zeros(2, dtype=float),
#         }

#     # Detects hands, face & pose,
#     # convert them into normalized landmark/keypoint coordinates in a 1D-array,
#     # and also returns the frame with the landmark connections drawn onto it
#     def parallelFeatureExtraction(
#         self, handDetector, faceDetector, poseDetector, frame, draw=True
#     ):
#         frameSize = (frame.shape[1], frame.shape[0])
#         with ThreadPoolExecutor() as executor:
#             t1 = executor.submit(self.detectHands, handDetector, frame, frameSize, draw)
#             t2 = executor.submit(self.detectPose, poseDetector, frame, frameSize, draw)
#             t3 = executor.submit(self.detectFace, faceDetector, frame, frameSize, draw)

#             # Convert results into 1D-array
#             detectionResults = self.flatten2dList(
#                 [
#                     self.flattenDetectionResult(t1.result()[0]),
#                     self.flattenDetectionResult(t1.result()[1]),
#                     t2.result(),
#                     t3.result()["bbox"],
#                     t3.result()["center"],
#                     t3.result()["center"] - t1.result()[0]["center"],
#                     t3.result()["center"] - t1.result()[1]["center"],
#                 ],
#                 dataType=float,
#             )

#             return detectionResults, frame

#     # Offset and normalize the landmark list
#     # Returns a 1d numpy array
#     def preprocess_landmarks(self, landmark_list, frameSize):
#         np_landmark_list = np.array(landmark_list, dtype=float)
#         np_frameSize = np.array([frameSize[0], frameSize[1], frameSize[0]])
#         return (np_landmark_list / np_frameSize).ravel()


#     # Offset and normalize a BBOX list (BBOX = Bounding Box, used in face and hand detection)
#     # Returns a 1d numpy array
#     def preprocess_bbox(self, bbox, frameSize):
#         bbox = np.array(bbox, dtype=float)
#         # Convert 3rd and 4th element into coordinates instead of width/height
#         bbox[2] = bbox[0] + bbox[2]
#         bbox[3] = bbox[1] + bbox[3]

#         # Normalize against frame size
#         bbox[0] /= frameSize[0]
#         bbox[1] /= frameSize[1]
#         bbox[2] /= frameSize[0]
#         bbox[3] /= frameSize[1]

#         return bbox


#     # Normalize a center vertex (a list of 2 elements)
#     # Returns a 1d numpy array
#     def preprocess_center(self, center, frameSize):
#         center = np.array(center, dtype=float)
#         center[0] /= frameSize[0]
#         center[1] /= frameSize[1]
#         return center


#     # Preprocess (Offset and normalize) the body's landmark list, bbox and center
#     def preprocess_body_part(self, bodyPart, frameSize):
#         bodyPart["lmList"] = self.preprocess_landmarks(bodyPart["lmList"], frameSize)
#         bodyPart["bbox"] = self.preprocess_bbox(bodyPart["bbox"], frameSize)
#         bodyPart["center"] = self.preprocess_center(bodyPart["center"], frameSize)
#         return bodyPart


#     # Function to generate empty/placeholder data for a hand
#     # Used when a hand is not detected in frame
#     def generate_empty_hand(self, type):
#         return {
#             "lmList": np.zeros(63, dtype=float),
#             "bbox": np.zeros(4, dtype=float),
#             "center": np.zeros(2, dtype=float),
#             "type": type,
#         }


#     # Select the best matching face, aka the one with the best score (clarity)
#     # and closest to the center of the screen
#     # Since the Neural network will be design to only accept one face
#     def select_best_matching_face(self, faces, frameSize):
#         if not faces or len(faces) == 0:
#             return False
#         elif len(faces) == 1:
#             return faces[0]

#         def difference(a, b):
#             return ((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2)

#         frameCenter = (frameSize[0] / 2, frameSize[1] / 2)

#         best_score = faces[0]
#         best_center = faces[0]
#         center_diff = difference(faces[0]["center"], frameCenter)

#         for each in faces[1:]:
#             if difference(each["center"], frameCenter) < center_diff:
#                 best_center = each
#             if each["score"][0] > best_score["score"][0]:
#                 best_score = each

#         if best_center["score"][0] > 0.5:
#             return best_center
#         return best_score

#     # Flatten a 2d np array into 1d array
#     def flatten2dList(self, arr, dataType=float):
#         return np.fromiter(chain.from_iterable(arr), dataType)

#     # Flatten everything
#     def flattenDetectionResult(self, obj):
#         return np.concatenate([obj["lmList"], obj["bbox"], obj["center"]])


#     def extractFeatures(self, frame):
#         detectionResults, frame = self.parallelFeatureExtraction(
#             self.handDetector, self.faceDetector, self.poseDetector, frame
#         )

#         return detectionResults, frame


# OLD ONE
class FeatureExtractionModule():
    def __init__(self, **kwargs):
        # Detectors
        self.handDetector = HandDetector(detectionCon=0.5, maxHands=2)
        self.faceDetector = FaceDetector(minDetectionCon=0.5)
        self.poseDetector = PoseDetector(detectionCon=0.5)

    def detectHands(self, handDetector, frame, frameSize, draw):
        results = None
        # Hand Detection
        if draw:
            results, frame = handDetector.findHands(frame, draw=draw, flipType=False)
        else:
            results = handDetector.findHands(frame, draw=draw, flipType=False)

        if not results:
            results = [generate_empty_hand("Left"), generate_empty_hand("Right")]
        elif len(results) == 1:
            if results[0]["type"] == "Left":
                results[0] = preprocess_body_part(results[0], frameSize)
                results.append(generate_empty_hand("Right"))
            else:
                results[0] = preprocess_body_part(results[0], frameSize)
                results.insert(0, generate_empty_hand("Left"))
        else:
            results[0] = preprocess_body_part(results[0], frameSize)
            results[1] = preprocess_body_part(results[1], frameSize)
        return results

    # Pose Detection
    # **We only use the first 23 out of the total 33 landmark points
    #   as those represent the lower half body and are irrelevant to sign language interpretation
    def detectPose(self, poseDetector, frame, draw):
        frame = poseDetector.findPose(frame, draw=draw)
        results, _ = poseDetector.findPosition(frame, bboxWithHands=False)
        if results:
            results = preprocess_landmarks(results[:23])
        else:
            results = np.zeros(23, dtype=int)
        return results

    # Face Detection
    def detectFace(self, faceDetector, frame, frameSize, draw):
        frame, results = faceDetector.findFaces(frame, draw=draw)
        if results:
            results = select_best_matching_face(results, frameSize)
            results["bbox"] = preprocess_bbox(results["bbox"], frameSize)
            results["center"] = preprocess_center(results["center"], frameSize)
        else:
            results = {
                "bbox": np.zeros(4, dtype=float),
                "center": np.zeros(2, dtype=float),
            }
        return results

    # Detects hands, face & pose,
    # convert them into normalized landmark/keypoint coordinates in a 1D-array,
    # and also returns the frame with the landmark connections drawn onto it
    def parallelFeatureExtraction(
        self, handDetector, faceDetector, poseDetector, frame, draw=True
    ):
        frameSize = (frame.shape[1], frame.shape[0])
        with ThreadPoolExecutor() as executor:
            t1 = executor.submit(self.detectHands, handDetector, frame, frameSize, draw)
            t2 = executor.submit(self.detectPose, poseDetector, frame, draw)
            t3 = executor.submit(self.detectFace, faceDetector, frame, frameSize, draw)

            # Convert results into 1D-array
            detectionResults = flatten2dList(
                [
                    flattenDetectionResult(t1.result()[0]),
                    flattenDetectionResult(t1.result()[1]),
                    t2.result(),
                    t3.result()["bbox"],
                    t3.result()["center"],
                    t3.result()["center"] - t1.result()[0]["center"],
                    t3.result()["center"] - t1.result()[1]["center"],
                ],
                dataType=float,
            )

            return detectionResults, frame


    def extractFeatures(self, frame):

        detectionResults, frame = self.parallelFeatureExtraction(
            self.handDetector, self.faceDetector, self.poseDetector, frame
        )

        return detectionResults, frame
