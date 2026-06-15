import cv2
import os
import mediapipe as mp
from gui import App
from trainer_logic import SquatTrainer
from voice_commands import VoiceAssistant
import time
from db_manager import init_db, save_session


def getCameras(max_cams=10):
    cameras = []

    for i in range(max_cams):
        cap = cv2.VideoCapture(i)

        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                cameras.append(i)

        cap.release()

    return cameras


def main():
    init_db()  # ДОДАНО: створення таблиці БД, якщо її нема
    gui = App()
    trainer = SquatTrainer()
    
    #USE_CAMERA_2 = True  # Зміни на True, коли підключиш другу камеру
    
    print("Created squat trainer")
    #cap_1 = cv2.VideoCapture(0)
    #if USE_CAMERA_2:
        #cap_2 = cv2.VideoCapture(1)
    #else:
        #cap_2 = None

    cams_idxs = getCameras()

    cap_1 = None
    cap_2 = None

    if len(cams_idxs) > 0:
        cap_1 = cv2.VideoCapture(cams_idxs[0])

    if len(cams_idxs) > 1:
        print(cams_idxs)
        cap_2 = cv2.VideoCapture(cams_idxs[1])

    if cap_1 is None:
        print("No cameras found")
        return
    
    print("cameras onboard")
    # Прибираємо примусові налаштування для IP-камери
    if cap_1 is not None and cap_1.isOpened():
        cap_1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap_1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap_1.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
    # Для cap_2 (DroidCam по Wi-Fi) нічого не задаємо через .set()!
    print("setted cameras")
    assistant = VoiceAssistant(trainer.state)
    print("created assistant")
    assistant.start()
    print("started assistant")

    def save_current_session():
        """ДОДАНО: Допоміжна функція для збереження даних у БД"""
        if trainer.state.get("is_training") and trainer.state.get("start_time", 0) > 0:
            duration = time.time() - trainer.state["start_time"]
            save_session(
                duration=duration,
                reps_done=trainer.state["reps"],
                target_reps=trainer.state["target_reps"],
                error_count=trainer.state.get("session_error_count", 0)
            )
            trainer.state["start_time"] = 0  # Скидаємо, щоб не зберегти двічі

    def on_stop():
        assistant.is_listening = False  # Спочатку зупиняємо потік мікрофона
        save_current_session() # Зберігаємо перед ручною зупинкою з інтерфейсу
        trainer.state["quit"] = True

    gui.btn_stop.configure(command=on_stop)
    frame_counter = 0

    def run_loop():
        nonlocal frame_counter

        if trainer.state.get("quit", False):
            save_current_session()  # Зберігаємо, якщо вихід був через голос
            if cap_1 is not None:
                cap_1.release()
            if cap_2 is not None:
                cap_2.release()
            gui.destroy()
            os._exit(0)
            
        ret1, frame1 = cap_1.read()
        if not ret1:
            gui.after(100, run_loop)
            return

        # Відзеркалюємо по горизонталі для фронтального виду, щоб рухи були інтуїтивно зрозумілими для користувача
        # Цифра 1 означає віддзеркалення по горизонталі (y-axis)
        frame1 = cv2.flip(frame1, 1)
        
        # Логіка для другої камери
        if  cap_2 is not None:
            ret2, frame2 = cap_2.read()
            if not ret2:
                frame2 = frame1.copy()
        else:
            frame2 = frame1.copy()  # Примусово дублюємо для правого вікна

        #  print("PROCESSING SIDE VIEW...")
        res_side, err_side = trainer.process_side_view(frame2)

        all_errors = list(err_side)

        if frame_counter % 1 == 0:
            # print("PROCESSING FRONT VIEW...")
            trainer.last_front_res, trainer.last_front_err = trainer.process_front_view(
                frame1
            )

        all_errors.extend(trainer.last_front_err)

        # print("DRAWING...")
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

        # print("UPDATING GUI...")
        gui.reps_label.configure(text=f"REPS: {trainer.state['reps']}")
        gui.error_label.configure(text=" | ".join(all_errors))
        gui.update_cameras(frame1, frame2)

        # print("DEBUG: Frame processed")
        frame_counter += 1
        gui.after(15, run_loop) # Замість 30 можна поставити 15 для більшої плавності, але це збільшить навантаження на CPU

    print("STEP 5: Launching GUI Loop...")
    gui.after(100, run_loop)
    gui.mainloop()


if __name__ == "__main__":
    main()

