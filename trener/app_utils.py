import mediapipe as mp
from tts import speak
from detection_utils import detect_pose, check_technique, USER_POSE
from tracker_utils import (
    get_body_points,
    get_all_angles,
    update_tracker,
)


def setup_mediapipe():
    mp_pose = mp.solutions.pose
    model = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=0,  # 0 — самое легкое решение, уберет фризы
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    return model, mp_pose


def run_analysis(results, current_state, p_tracker, e_tracker):
    pts = get_body_points(results.pose_landmarks.landmark)
    ang = get_all_angles(pts)

    raw_p = detect_pose(ang["lka"], ang["rka"], ang["lha"], ang["rha"])
    confirmed_p = update_tracker(raw_p, p_tracker, 3)
    if confirmed_p is not None:
        current_state["pose"] = confirmed_p

    raw_e = []
    if current_state["pose"] in [USER_POSE.DOWN.value, USER_POSE.NOT_ENOUGH.value]:
        raw_e = check_technique(**ang)

    confirmed_e = update_tracker(raw_e, e_tracker, 3)
    if confirmed_e is not None:
        e_tracker["current"] = confirmed_e
        handle_voice_feedback(confirmed_e, e_tracker)

    return ang


def handle_voice_feedback(errors, e_tracker):
    if errors and errors != e_tracker["spoken"]:
        speak(". ".join(errors))
        e_tracker["spoken"] = errors
    elif not errors:
        e_tracker["spoken"] = []
