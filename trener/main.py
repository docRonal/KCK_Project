import cv2
import mediapipe as mp
from tts import speak
from detection_utils import USER_POSE
from tracker_utils import process_exercise_logic
from interface import render_ui
from app_utils import setup_mediapipe, run_analysis


def main():
    state = {"reps": 0, "goal": False, "pose": USER_POSE.UP.value}
    p_tracker = {"last": None, "count": 0}
    e_tracker = {"last": [], "count": 0, "current": [], "spoken": []}

    model, mp_pose = setup_mediapipe()
    cap = cv2.VideoCapture(1)
    speak("System ready.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            run_analysis(results, state, p_tracker, e_tracker)

            state["goal"], state["reps"] = process_exercise_logic(
                state["pose"], state["goal"], state["reps"]
            )

            render_ui(
                frame, state["reps"], state["pose"], state["goal"], e_tracker["current"]
            )

        cv2.imshow("Trainer", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
