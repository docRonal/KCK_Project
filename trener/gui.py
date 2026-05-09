import customtkinter as ctk
import cv2
from PIL import Image
import mediapipe as mp
from trainer_logic import SquatTrainer
# from interface import render_ui


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Trainer")
        self.geometry("2000x800")
        self.configure(fg_color="#242424")
        self.trainer = SquatTrainer()
        self.cap = cv2.VideoCapture(1)

        self.video_label = ctk.CTkLabel(self, text="")
        self.video_label.pack(pady=10, padx=10, fill="both", expand=True)

        self.info_label = ctk.CTkLabel(
            self,
            text="REPS: 0 | STATE: UP",
            font=("Arial", 32, "bold"),
            text_color="#00FF00",
        )
        self.info_label.pack(pady=(20, 10))

        self.btn_quit = ctk.CTkButton(
            self,
            text="STOP",
            command=self.force_exit,
            width=300,
            height=60,
            font=("Arial", 20, "bold"),
            fg_color="#cc0000",
            hover_color="#ff0000",
        )
        self.btn_quit.pack(pady=(10, 30))

        self.update_loop()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_loop(self):
        ret, frame = self.cap.read()
        if ret:
            results, state, errors = self.trainer.process_frame(frame)

            if results and results.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, results.pose_landmarks, self.trainer.mp_pose.POSE_CONNECTIONS
                )
                # render_ui(frame, state["reps"], state["pose"], state["goal"], errors)

            self.info_label.configure(
                text=f"REPS: {state['reps']} | STATE: {state['pose']}"
            )

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(800, 500))

            self.video_label.configure(image=ctk_img)
            self.video_label.image = ctk_img

        self.after(10, self.update_loop)

    def on_closing(self):
        self.cap.release()
        self.destroy()

    def force_exit(self):
        if hasattr(self, "cap") and self.cap.isOpened():
            self.cap.release()
        self.destroy()
        import os

        os._exit(0)
