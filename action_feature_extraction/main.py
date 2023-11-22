import numpy as np
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.PoseModule import PoseDetector
from concurrent.futures import ThreadPoolExecutor

from .cvzone_preprocess import *

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
