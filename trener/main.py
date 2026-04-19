import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import cv2
import mediapipe as mp
import numpy as np
from enum import Enum
import pyttsx3
import threading
import time

POSE_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5), (5, 6), (6, 8), (9, 10),
    (11, 12), (11, 13), (13, 15), (15, 17), (15, 19), (15, 21), (17, 19),
    (12, 14), (14, 16), (16, 18), (16, 20), (16, 22), (18, 20),
    (11, 23), (12, 24), (23, 24), (23, 25), (24, 26), (25, 27), (26, 28),
    (27, 29), (28, 30), (29, 31), (30, 32), (27, 31), (28, 32)
]

def draw_landmarks_manual(image, landmarks, connections):
    # Draw landmarks and connections manually (for debugging or custom visualization)
    h, w, c = image.shape
    
    # Draw lines (connections between points)
    for connection in connections:
        start_idx, end_idx = connection[0], connection[1]
        if start_idx < len(landmarks) and end_idx < len(landmarks):
            start_point = (int(landmarks[start_idx].x * w), int(landmarks[start_idx].y * h))
            end_point = (int(landmarks[end_idx].x * w), int(landmarks[end_idx].y * h))
            cv2.line(image, start_point, end_point, (255, 255, 255), 2)
            
    # Draw points
    for landmark in landmarks:
        point = (int(landmark.x * w), int(landmark.y * h))
        cv2.circle(image, point, 4, (0, 0, 255), -1)

is_speaking = False

def tts_task(text):
    global is_speaking
    try:
        import pythoncom
        pythoncom.CoInitialize()
    except ImportError:
        pass
        
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Audio Error: {e}")
    finally:
        is_speaking = False

def speak(text):
    global is_speaking
    if not is_speaking:
        is_speaking = True
        threading.Thread(target=tts_task, args=(text,), daemon=True).start()

class USER_POSE(Enum):
    UP = 0
    DOWN = 1
    TOO_DEEP = 2
    NOT_ENOUGH = 3
    UNKNOWN = 4
    UNKNOWN_SIDE = 7

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def check_technique(lka, rka, lha, rha, laa, raa):
    errors = []
    if lka < 80 or rka < 80:
        errors.append("KNEE OVER TOE")
        
    front_hip = min(lha, rha)
    
    if front_hip < 60:
        errors.append("LEANING FORWARD")
    elif front_hip > 135:
        errors.append("BACK NOT STRAIGHT")
        
    if laa < 75 or raa < 75:
        errors.append("HEEL LIFTED")
    return errors

def detect_side(lha, rha, t):
    if abs(90 - lha) < t and abs(180 - rha) < t:
        return "l"
    elif abs(180 - lha) < t and abs(90 - rha) < t:
        return "r"
    return "n"

def detect_pose(lka, rka, lha, rha):
    up_tol = 15
    down_tol = 20

    if all(abs(170 - a) < up_tol for a in [lka, rka, lha, rha]):
        return USER_POSE.UP.value

    if abs(90 - lka) < down_tol and abs(90 - rka) < down_tol:
        return USER_POSE.DOWN.value

    if lka < 65 or rka < 65:
        return USER_POSE.TOO_DEEP.value

    if (65 < lka < 160) and (65 < rka < 160):
        return USER_POSE.NOT_ENOUGH.value

    return USER_POSE.UNKNOWN.value

def main():
    rep_counter = 0
    goal_reached = False

    current_confirmed_pose = USER_POSE.UP.value
    pose_tracker = {"last_pose": None, "count": 0}
    error_tracker = {"current_errors": [], "pending_errors": [], "count": 0, "spoken_errors": []}
    SMOOTH_FRAMES = 3

    # New MediaPipe API usage
    BaseOptions = mp.tasks.BaseOptions
    PoseLandmarker = mp.tasks.vision.PoseLandmarker
    PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    # Path to the pose landmarker model (ensure this file is in the same directory or provide the correct path)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'pose_landmarker_lite.task')
    
    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.VIDEO
    )

    cap = cv2.VideoCapture(0)
    speak("System ready. Let's start training.")

    # Fix the start time for timestamp generation
    start_time = time.time()

    # Initialize the PoseLandmarker
    with PoseLandmarker.create_from_options(options) as landmarker:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 1. Prepare the frame for the new API
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            # Timestamps must be strictly increasing for video mode
            timestamp_ms = int((time.time() - start_time) * 1000)

            # 2. Frame process
            pose_result = landmarker.detect_for_video(mp_image, timestamp_ms)

            # 3. If body landmarks are found
            if pose_result.pose_landmarks:
                
                # --- Scelet drawing ---
                for pose_landmarks in pose_result.pose_landmarks:
                    draw_landmarks_manual(frame, pose_landmarks, POSE_CONNECTIONS)

                # Basic landmark access using new API structure
                lm = pose_result.pose_landmarks[0]

                def get_p(idx):
                    return [lm[idx].x, lm[idx].y]

                # Get relevant landmarks
                l_sh, r_sh = get_p(11), get_p(12)
                l_hip, r_hip = get_p(23), get_p(24)
                l_knee, r_knee = get_p(25), get_p(26)
                l_ank, r_ank = get_p(27), get_p(28)
                l_ft, r_ft = get_p(31), get_p(32)

                # Calculate angles
                lka = calculate_angle(l_hip, l_knee, l_ank)
                rka = calculate_angle(r_hip, r_knee, r_ank)
                lha = calculate_angle(l_sh, l_hip, l_knee)
                rha = calculate_angle(r_sh, r_hip, r_knee)
                laa = calculate_angle(l_knee, l_ank, l_ft)
                raa = calculate_angle(r_knee, r_ank, r_ft)

                # Detect pose
                raw_pose = detect_pose(lka, rka, lha, rha)

                # Smooth pose tracking
                if raw_pose == pose_tracker["last_pose"]:
                    pose_tracker["count"] += 1
                else:
                    pose_tracker["last_pose"] = raw_pose
                    pose_tracker["count"] = 0

                if pose_tracker["count"] >= SMOOTH_FRAMES:
                    current_confirmed_pose = raw_pose

                if current_confirmed_pose == USER_POSE.DOWN.value:
                    goal_reached = True

                if current_confirmed_pose == USER_POSE.UP.value and goal_reached:
                    rep_counter += 1
                    goal_reached = False

                # Check technique only when in DOWN or NOT_ENOUGH pose
                raw_errors = []
                if current_confirmed_pose in [
                    USER_POSE.DOWN.value,
                    USER_POSE.NOT_ENOUGH.value,
                ]:
                    raw_errors = check_technique(lka, rka, lha, rha, laa, raa)

                # Smooth error tracking
                if raw_errors == error_tracker["pending_errors"]:
                    error_tracker["count"] += 1
                else:
                    error_tracker["pending_errors"] = raw_errors
                    error_tracker["count"] = 0

                if error_tracker["count"] >= SMOOTH_FRAMES:
                    error_tracker["current_errors"] = raw_errors
                    
                    # Voice feedback for errors
                    if raw_errors and raw_errors != error_tracker["spoken_errors"]:
                        error_message = ". ".join(raw_errors)
                        speak(error_message)
                        error_tracker["spoken_errors"] = raw_errors
                    elif not raw_errors:
                        error_tracker["spoken_errors"] = []

            # --- UI (HUD) ---
            cv2.putText(frame, f"REPS: {rep_counter}", (10, 50), 2, 1, (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"STATE: {USER_POSE(current_confirmed_pose).name}",
                (10, 100),
                2,
                0.7,
                (255, 255, 255),
                1,
            )
            
            if goal_reached:
                cv2.putText(frame, "GO UP!", (10, 130), 2, 0.7, (0, 255, 255), 2)

            for i, err in enumerate(error_tracker["current_errors"]):
                cv2.putText(frame, err, (10, 170 + (i * 30)), 2, 0.8, (0, 0, 255), 2)

            cv2.imshow("Lunge Analysis", frame)
            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()