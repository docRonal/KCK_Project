import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture("film.mp4")
pose = mp_pose.Pose()
_, frame = cap.read()
results = pose.process(frame)
landmarks = results.pose_landmarks.landmark
ramie_lewe = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]

