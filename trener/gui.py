import customtkinter as ctk
import cv2
from PIL import Image
import mediapipe as mp
import numpy as np  # Понадобится для склейки кадров
import os
from trainer_logic import SquatTrainer


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Trainer - Dual View")
        self.geometry("1600x900")
        self.configure(fg_color="#242424")
        self.trainer = SquatTrainer()

        self.cap_front = cv2.VideoCapture(1)
        self.cap_side = cv2.VideoCapture(0)

        self.info_label = ctk.CTkLabel(
            self,
            text="REPS: 0 | STATE: UP",
            font=("Arial", 32, "bold"),
            text_color="#00FF00",
        )
        self.info_label.pack(pady=(20, 10))

        self.video_label = ctk.CTkLabel(self, text="")
        self.video_label.pack(pady=10, padx=10, fill="both", expand=True)

        self.btn_quit = ctk.CTkButton(
            self,
            text="STOP (Q)",
            command=self.force_exit,
            width=300,
            height=60,
            font=("Arial", 20, "bold"),
            fg_color="#cc0000",
            hover_color="#ff0000",
        )
        self.btn_quit.pack(pady=(10, 30))

        self.bind("<KeyPress-q>", lambda e: self.force_exit())
        self.bind("<KeyPress-Q>", lambda e: self.force_exit())

        self.update_loop()
        self.protocol("WM_DELETE_WINDOW", self.force_exit)

    def update_loop(self):
        ret_f, frame_f = self.cap_front.read()
        ret_s, frame_s = self.cap_side.read()

        if ret_f and ret_s:
            frame_f = cv2.resize(frame_f, (640, 480))
            frame_s = cv2.resize(frame_s, (640, 480))
            results, state, errors = self.trainer.process_frame(frame_f)

            if results and results.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame_f,
                    results.pose_landmarks,
                    self.trainer.mp_pose.POSE_CONNECTIONS,
                )

            combined_frame = cv2.hconcat([frame_f, frame_s])

            self.info_label.configure(
                text=f"REPS: {state['reps']} | STATE: {state['pose']}"
            )

            img = Image.fromarray(cv2.cvtColor(combined_frame, cv2.COLOR_BGR2RGB))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(1280, 480))

            self.video_label.configure(image=ctk_img)
            self.video_label.image = ctk_img

        self.after(10, self.update_loop)

    def force_exit(self):
        if hasattr(self, "cap_front") and self.cap_front.isOpened():
            self.cap_front.release()
        if hasattr(self, "cap_side") and self.cap_side.isOpened():
            self.cap_side.release()

        self.destroy()
        os._exit(0)

    def on_closing(self):
        self.force_exit()

