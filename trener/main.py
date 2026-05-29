import cv2
import os
import mediapipe as mp
from gui import App
from trainer_logic import SquatTrainer
from voice_commands import VoiceAssistant

def list_cameras():
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Index {i}: Camera FOUND")
            cap.release()
        else:
            print(f"Index {i}: Not found")

def main():
    gui = App()
    trainer = SquatTrainer()
    print("Created squat trainer")
    list_cameras()
    cap_1 = cv2.VideoCapture(0)
    cap_2 = cv2.VideoCapture(1, cv2.CAP_MSMF)
    while True:
        ret, frame = cap_2.read()

        if not ret:
            print("NO FRAME")
            break

        cv2.imshow("cam", frame)

        if cv2.waitKey(1) == 27:
            break
 
    import time
    time.sleep(2)
    #cap_2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    print("cameras onboard")
    for c in [cap_1, cap_2]:
        if c.isOpened():
            c.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            c.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            c.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    print("setted cameras")
    assistant = VoiceAssistant(trainer.state)
    print("created assistant")
    assistant.start()
    print("started assistant")

    def on_stop():
        trainer.state["quit"] = True

    gui.btn_stop.configure(command=on_stop)
    frame_counter = 0

    def run_loop():
        nonlocal frame_counter

        if trainer.state.get("quit", False):
            cap_1.release()
            cap_2.release()
            gui.destroy()
            os._exit(0)
        print("READING CAMERAS...")
        ret1, frame1 = cap_1.read()
        ret2, frame2 = cap_2.read()
        if not ret1:
            print("CAMERA 1 FAILED")
            gui.after(100, run_loop)
            return

        if not ret2:
            print("CAMERA 2 FAILED - CLONING FRAME 1")
            frame2 = frame1.copy()
            ret2 = True

        print("PROCESSING SIDE VIEW...")
        res_side, err_side = trainer.process_side_view(frame2)

        all_errors = list(err_side)

        if frame_counter % 30 == 0:
            print("PROCESSING FRONT VIEW...")
            trainer.last_front_res, trainer.last_front_err = trainer.process_front_view(
                frame1
            )

        all_errors.extend(trainer.last_front_err)

        print("DRAWING...")
        if res_side and res_side.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame2, res_side.pose_landmarks, trainer.mp_pose.POSE_CONNECTIONS
            )

        if trainer.last_front_res and trainer.last_front_res.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame1,
                trainer.last_front_res.pose_landmarks,
                trainer.mp_pose.POSE_CONNECTIONS,
            )

        print("UPDATING GUI...")
        gui.reps_label.configure(text=f"REPS: {trainer.state['reps']}")
        gui.error_label.configure(text=" | ".join(all_errors))
        gui.update_cameras(frame1, frame2)

        print("DEBUG: Frame processed")
        frame_counter += 1
        gui.after(100, run_loop)

    print("STEP 5: Launching GUI Loop...")
    gui.after(100, run_loop)
    gui.mainloop()


if __name__ == "__main__":
    main()
