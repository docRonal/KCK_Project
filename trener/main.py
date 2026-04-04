import cv2
import mediapipe as mp
import numpy as np
from enum import Enum


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
    if lha < 70 or rha < 70:
        errors.append("LEANING FORWARD")
    if 75 < lha < 105 and 75 < rha < 105:
        pass
    elif (lha > 110 or rha > 110) and (lha < 160 or rha < 160):
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

    if (65 < lka < 160) or (65 < rka < 160):
        return USER_POSE.NOT_ENOUGH.value

    return USER_POSE.UNKNOWN.value


def main():
    rep_counter = 0
    goal_reached = False

    current_confirmed_pose = USER_POSE.UP.value
    pose_tracker = {"last_pose": None, "count": 0}
    error_tracker = {"current_errors": [], "pending_errors": [], "count": 0}
    SMOOTH_FRAMES = 3

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose_model = mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity=1
    )

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame.flags.writeable = False
        results = pose_model.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame.flags.writeable = True

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )
            lm = results.pose_landmarks.landmark

            def get_p(idx):
                return [lm[idx].x, lm[idx].y]

            l_sh, r_sh = get_p(11), get_p(12)
            l_hip, r_hip = get_p(23), get_p(24)
            l_knee, r_knee = get_p(25), get_p(26)
            l_ank, r_ank = get_p(27), get_p(28)
            l_ft, r_ft = get_p(31), get_p(32)

            lka = calculate_angle(l_hip, l_knee, l_ank)
            rka = calculate_angle(r_hip, r_knee, r_ank)
            lha = calculate_angle(l_sh, l_hip, l_knee)
            rha = calculate_angle(r_sh, r_hip, r_knee)
            laa = calculate_angle(l_knee, l_ank, l_ft)
            raa = calculate_angle(r_knee, r_ank, r_ft)

            raw_pose = detect_pose(lka, rka, lha, rha)

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

            raw_errors = []
            if current_confirmed_pose in [
                USER_POSE.DOWN.value,
                USER_POSE.NOT_ENOUGH.value,
            ]:
                raw_errors = check_technique(lka, rka, lha, rha, laa, raa)

            if raw_errors == error_tracker["pending_errors"]:
                error_tracker["count"] += 1
            else:
                error_tracker["pending_errors"] = raw_errors
                error_tracker["count"] = 0

            if error_tracker["count"] >= SMOOTH_FRAMES:
                error_tracker["current_errors"] = raw_errors

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
