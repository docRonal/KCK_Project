# main.py (обновленная версия)
import cv2
import mediapipe as mp
from tts import speak
from detection_utils import USER_POSE
from tracker_utils import process_exercise_logic
from interface import render_ui
from app_utils import setup_mediapipe, run_analysis
from voice_commands import VoiceAssistant # <-- Подключаем новый модуль

def main():
    state = {
        "reps": 0, 
        "goal": False, 
        "pose": USER_POSE.UP.value,
        "is_training": False,  
        "quit": False,         
        "target_reps": 10     
    }
    p_tracker = {"last": None, "count": 0}
    e_tracker = {"last": [], "count": 0, "current": [], "spoken": []}

    model, mp_pose = setup_mediapipe()
    cap = cv2.VideoCapture(0)
    
    # Запускаем голосового ассистента
    assistant = VoiceAssistant(state)
    assistant.start()

    speak("System gotowy. Powiedz: trening.")

    while cap.isOpened() and not state["quit"]: 
        ret, frame = cap.read()
        if not ret:
            break

        results = model.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            if state["is_training"]:
                run_analysis(results, state, p_tracker, e_tracker)

                state["goal"], state["reps"] = process_exercise_logic(
                    state["pose"], state["goal"], state["reps"]
                )

            render_ui(
                frame, state["reps"], state["pose"], state["goal"], e_tracker["current"]
            )
            
            if not state["is_training"]:
                 cv2.putText(frame, "Powiedz 'Zacznij trening'", (10, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        cv2.imshow("Trener", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()