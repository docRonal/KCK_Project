import cv2
import mediapipe as mp
import numpy as np
from enum import Enum


class Lmarks(Enum):
    LEFT_SHOULDER = 0
    RIGHT_SHOULDER = 1
    LEFT_ELBOW = 2
    RIGHT_ELBOW = 3
    LEFT_WRIST = 4
    RIGHT_WRIST = 5
    LEFT_HIP = 6
    RIGHT_HIP = 7


def calculate_angle(hip, shoulder, elbow, w, h):
    hp_arr = np.array([hip.x * w, hip.y * h])
    sh_arr = np.array([shoulder.x * w, shoulder.y * h])
    el_arr = np.array([elbow.x * w, elbow.y * h])

    radians = np.arctan2(el_arr[1] - sh_arr[1], el_arr[0] - sh_arr[0]) - np.arctan2(
        hp_arr[1] - sh_arr[1], hp_arr[0] - sh_arr[0]
    )

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle
    return angle


def detect_letter(rangle, langle):
    abc = {"T": [90, 90], "I": [5, 5], "L": [170, 90], "Y": [135, 135]}
    tolerance = 10
    for key, value in abc.items():
        if abs(rangle - value[0]) < tolerance and abs(langle - value[1]) < tolerance:
            return key

    return "None"


def main():
    current_letter = "None"
    display_counter = 0
    CONFIRM_FRAMES = 15
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    pose_model = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if not cap.isOpened():
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose_model.process(rgb_frame)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )
            landmarks = results.pose_landmarks.landmark
            required_landmarks = [
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER],
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW],
                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW],
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST],
                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST],
                landmarks[mp_pose.PoseLandmark.LEFT_HIP],
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP],
            ]
            left_angle = calculate_angle(
                required_landmarks[Lmarks.LEFT_HIP.value],
                required_landmarks[Lmarks.LEFT_SHOULDER.value],
                required_landmarks[Lmarks.LEFT_ELBOW.value],
                width,
                height,
            )
            right_angle = calculate_angle(
                required_landmarks[Lmarks.RIGHT_HIP.value],
                required_landmarks[Lmarks.RIGHT_SHOULDER.value],
                required_landmarks[Lmarks.RIGHT_ELBOW.value],
                width,
                height,
            )
            l_visible = required_landmarks[Lmarks.LEFT_WRIST.value].visibility > 0.5
            r_visible = required_landmarks[Lmarks.RIGHT_WRIST.value].visibility > 0.5
            res = detect_letter(right_angle, left_angle)

            if l_visible and r_visible:
                if res != "None":
                    current_letter = res
                    display_counter = CONFIRM_FRAMES
                else:
                    if display_counter > 0:
                        display_counter -= 1
                    else:
                        current_letter = "None"
                if current_letter != "None":
                    cv2.putText(
                        frame,
                        f"{current_letter}",
                        (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        4,
                        (100, 50, 140),
                        5,
                    )

        cv2.imshow("Vebcam view", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
