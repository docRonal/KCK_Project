import cv2
import mediapipe as mp
import numpy as np

from detection_utils import detect_pose, check_technique, USER_POSE
from tracker_utils import (
    get_body_points,
    get_all_angles,
    update_tracker,
)


class SquatTrainer:
    def __init__(self):
        self.mp_pose = mp.solutions.pose

        self.model_front = self.mp_pose.Pose(model_complexity=0)
        self.model_side = self.mp_pose.Pose(model_complexity=0)

        self.state = {
            "reps": 0,
            "is_training": False,
            "quit": False,
            "pose": USER_POSE.UP.value,
            "target_reps": 10,
        }

        self.p_tracker = {"history": [], "current": None}
        self.e_tracker = {"history": [], "current": [], "spoken": []}

        self.last_front_res = None
        self.last_front_err = []

    def check_shoulder_line(self, landmarks):
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        diff = abs(left_shoulder.y - right_shoulder.y)

        if diff > 0.05:
            return ["Krzywe plecy!"]
        return []

    def process_front_view(self, frame):
        results = self.model_front.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        front_errors = []
        if results.pose_landmarks:
            front_errors = self.check_shoulder_line(results.pose_landmarks.landmark)
        return results, front_errors

    def process_side_view(self, frame):
        results = self.model_side.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        side_errors = []

        if results.pose_landmarks and self.state["is_training"]:
            landmarks = results.pose_landmarks.landmark
            pts = get_body_points(landmarks)
            ang = get_all_angles(pts)

            raw_p = detect_pose(ang["lka"], ang["rka"], ang["lha"], ang["rha"])
            confirmed_p = update_tracker(raw_p, self.p_tracker, 3)

            if confirmed_p is not None:
                if (
                    self.state["pose"] == USER_POSE.DOWN.value
                    and confirmed_p == USER_POSE.UP.value
                ):
                    self.state["reps"] += 1
                self.state["pose"] = confirmed_p

            if self.state["pose"] in [USER_POSE.DOWN.value, USER_POSE.NOT_ENOUGH.value]:
                raw_e = check_technique(**ang)
                confirmed_e = update_tracker(raw_e, self.e_tracker, 3)
                if confirmed_e is not None:
                    side_errors = confirmed_e

        return results, side_errors
