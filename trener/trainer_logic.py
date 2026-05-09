import cv2
from tts import speak
from detection_utils import USER_POSE
from tracker_utils import process_exercise_logic
from app_utils import setup_mediapipe, run_analysis


class SquatTrainer:
    def __init__(self):
        self.state = {"reps": 0, "goal": False, "pose": USER_POSE.UP.value}
        self.p_tracker = {"last": None, "count": 0}
        self.e_tracker = {"last": [], "count": 0, "current": [], "spoken": []}

        self.model, self.mp_pose = setup_mediapipe()

    def process_frame(self, frame):
        results = self.model.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.pose_landmarks:
            run_analysis(results, self.state, self.p_tracker, self.e_tracker)

            self.state["goal"], self.state["reps"] = process_exercise_logic(
                self.state["pose"], self.state["goal"], self.state["reps"]
            )

            return results, self.state, self.e_tracker["current"]

        return None, self.state, []
