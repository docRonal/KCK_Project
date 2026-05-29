import customtkinter as ctk
from PIL import Image
import cv2


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Trainer Dual-View Pro")
        self.geometry("1400x900")
        self.configure(fg_color="#121212")

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.reps_label = ctk.CTkLabel(
            self, text="REPS: 0", font=("Arial", 60, "bold"), text_color="#00FF41"
        )
        self.reps_label.grid(row=0, column=0, columnspan=2, pady=20)

        self.video_left = ctk.CTkLabel(
            self, text="", fg_color="#1e1e1e", corner_radius=12
        )
        self.video_left.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.video_right = ctk.CTkLabel(
            self, text="", fg_color="#1e1e1e", corner_radius=12
        )
        self.video_right.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.error_label = ctk.CTkLabel(
            self, text="", font=("Arial", 24), text_color="#FF4444", wraplength=1000
        )
        self.error_label.grid(row=2, column=0, columnspan=2, pady=10)

        self.btn_stop = ctk.CTkButton(
            self,
            text="STOP SESSION",
            width=600,
            height=80,
            font=("Arial", 28, "bold"),
            fg_color="#B20000",
            hover_color="#FF0000",
            corner_radius=15,
        )
        self.btn_stop.grid(row=3, column=0, columnspan=2, pady=30)

    def update_cameras(self, frame_left, frame_right):
        img_l = Image.fromarray(cv2.cvtColor(frame_left, cv2.COLOR_BGR2RGB))
        ctk_l = ctk.CTkImage(light_image=img_l, dark_image=img_l, size=(600, 450))
        self.video_left.configure(image=ctk_l, text="")
        self.video_left.image = ctk_l

        img_r = Image.fromarray(cv2.cvtColor(frame_right, cv2.COLOR_BGR2RGB))
        ctk_r = ctk.CTkImage(light_image=img_r, dark_image=img_r, size=(600, 450))
        self.video_right.configure(image=ctk_r, text="")
        self.video_right.image = ctk_r
