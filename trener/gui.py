import customtkinter as ctk
from PIL import Image
import cv2
from history_gui import HistoryWindow

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Trainer Dual-View Pro")
        self.geometry("1400x900")
        self.configure(fg_color="#121212")

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- ДОДАНО: Плашка статусу ---
        self.status_label = ctk.CTkLabel(
            self, text="TRAINER IS OFF", font=("Arial", 45, "bold"), text_color="#B20000"
        )
        self.status_label.grid(row=0, column=0, pady=20)

        # --- ЗМІНЕНО: Зсуваємо лічильник повторень в 1-шу колонку ---
        self.reps_label = ctk.CTkLabel(
            self, text="REPS: 0", font=("Arial", 60, "bold"), text_color="#00FF41"
        )
        self.reps_label.grid(row=0, column=1, pady=20) # Прибрано columnspan=2

        # ПРОВЕРЬ ТУТ: self.video_left должен быть объявлен именно так
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
        
        # --- Кнопка історії ---
        self.btn_history = ctk.CTkButton(
            self,
            text="TRAINING HISTORY",
            width=600,
            height=60,
            font=("Arial", 24, "bold"),
            fg_color="#1f538d",
            hover_color="#14375e",
            corner_radius=15,
            command=self.open_history
        )
        self.btn_history.grid(row=4, column=0, columnspan=2, pady=10)
    
    # --- Метод відкриття вікна ---
    def open_history(self):
        HistoryWindow(self)

    def update_cameras(self, frame_left, frame_right):
        # Используем фиксированные размеры, чтобы Tkinter не "схлопывал" виджеты
        img_l = Image.fromarray(cv2.cvtColor(frame_left, cv2.COLOR_BGR2RGB))
        ctk_l = ctk.CTkImage(light_image=img_l, dark_image=img_l, size=(600, 450))
        self.video_left.configure(image=ctk_l, text="")  # Убираем текст загрузки
        self.video_left.image = ctk_l

        img_r = Image.fromarray(cv2.cvtColor(frame_right, cv2.COLOR_BGR2RGB))
        ctk_r = ctk.CTkImage(light_image=img_r, dark_image=img_r, size=(600, 450))
        self.video_right.configure(image=ctk_r, text="")
        self.video_right.image = ctk_r
