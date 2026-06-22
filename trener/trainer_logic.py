import cv2
import mediapipe as mp
import numpy as np

# Импортируем утилиты
from detection_utils import detect_pose, check_technique, USER_POSE
from tracker_utils import (
    get_body_points,
    get_all_angles,
    update_tracker,
)


class SquatTrainer:
    def __init__(self):
        self.mp_pose = mp.solutions.pose

        # Две независимые модели для стабильности на Intel Arc
        self.model_front = self.mp_pose.Pose(model_complexity=0)
        self.model_side = self.mp_pose.Pose(model_complexity=0)

        # Общее состояние
        self.state = {
            "reps": 0,
            "is_training": False,
            "quit": False,
            "pose": USER_POSE.UP.value,
            "target_reps": 10, # Цільова кількість повторень
            "start_time": 0.0,
            "session_error_count": 0,
            "goal_reached": False
        }

        # Трекеры для фильтрации поз и ошибок
        self.p_tracker = {
            "last": None, 
            "count": 0, 
            "history": [], 
            "current": None
        }
        self.e_tracker = {
            "last": [], 
            "count": 0, 
            "history": [], 
            "current": [], 
            "spoken": [], 
            "last_counted": []
        }

        # Кэш для фронтальной камеры
        self.last_front_res = None
        self.last_front_err = []

    def check_shoulder_line(self, landmarks):
        """Логика для фронтальной камеры"""
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        diff = abs(left_shoulder.y - right_shoulder.y)

        if diff > 0.05:  # Порог 5%
            return ["Krzywe plecy!"]
        return []

    def process_front_view(self, frame):
        """Минимальная обработка фронталки"""
        results = self.model_front.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        front_errors = []
        if results.pose_landmarks:
            front_errors = self.check_shoulder_line(results.pose_landmarks.landmark)
        return results, front_errors

    def process_side_view(self, frame):
        """Основная логика приседаний (Side View)"""
        results = self.model_side.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        side_errors = []

        if results.pose_landmarks and self.state["is_training"]:
            # Используем твою логику из app_utils/tracker_utils
            landmarks = results.pose_landmarks.landmark
            pts = get_body_points(landmarks)
            ang = get_all_angles(pts)

            # Определение позы (UP, DOWN и т.д.)
            raw_p = detect_pose(ang["lka"], ang["rka"], ang["lha"], ang["rha"])
            confirmed_p = update_tracker(raw_p, self.p_tracker, 3)

            # Логіка підрахунку повторень
            if confirmed_p is not None:
                # 1. Фіксуємо досягнення нижньої точки (DOWN або TOO_DEEP)
                if confirmed_p in [USER_POSE.DOWN.value, USER_POSE.TOO_DEEP.value]:
                    self.state["goal_reached"] = True
                
                # 2. Якщо користувач повернувся у верхню точку (UP) і перед цим був внизу
                elif confirmed_p == USER_POSE.UP.value and self.state.get("goal_reached", False):
                    self.state["reps"] += 1
                    self.state["goal_reached"] = False  # Скидаємо прапорець для наступного повторення
                
                # Оновлюємо поточну позу
                self.state["pose"] = confirmed_p

            # Проверка техники только в нижней точке
            if self.state["pose"] in [USER_POSE.DOWN.value, USER_POSE.NOT_ENOUGH.value]:
                raw_e = check_technique(**ang)
                confirmed_e = update_tracker(raw_e, self.e_tracker, 3)
                if confirmed_e is not None:
                    # ДОДАНО: Логіка підрахунку нових унікальних помилок
                    if confirmed_e and confirmed_e != self.e_tracker.get("last_counted", []):
                        self.state["session_error_count"] += len(confirmed_e)
                        self.e_tracker["last_counted"] = confirmed_e
                    elif not confirmed_e:
                        self.e_tracker["last_counted"] = []
                    
                    side_errors = confirmed_e
                    # Здесь можно вызвать speak из tts, если нужно

        return results, side_errors
