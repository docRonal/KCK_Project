import cv2
from detection_utils import USER_POSE


def render_ui(frame, reps, pose, goal, errors):
    cv2.imshow(frame)
