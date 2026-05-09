import cv2
from detection_utils import USER_POSE


def render_ui(frame, reps, pose, goal, errors):
    cv2.putText(frame, f"REPS: {reps}", (10, 50), 2, 1, (0, 255, 0), 2)
    cv2.putText(
        frame, f"STATE: {USER_POSE(pose).name}", (10, 100), 2, 0.7, (255, 255, 255), 1
    )
    if goal:
        cv2.putText(frame, "GO UP!", (10, 130), 2, 0.7, (0, 255, 255), 2)
    for i, err in enumerate(errors):
        cv2.putText(frame, err, (10, 170 + (i * 30)), 2, 0.8, (0, 0, 255), 2)
