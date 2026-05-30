import numpy as np
from enum import Enum


class USER_POSE(Enum):
    UP = 0
    DOWN = 1
    TOO_DEEP = 2
    NOT_ENOUGH = 3
    UNKNOWN = 4
    UNKNOWN_SIDE = 7


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle


def check_technique(lka, rka, lha, rha, laa, raa):
    errors = []
    if lka < 80 or rka < 80:
        errors.append("KNEE OVER TOE")

    front_hip = min(lha, rha)

    if front_hip < 60:
        errors.append("LEANING FORWARD")

    if laa < 75 or raa < 75:
        errors.append("HEEL LIFTED")
    return errors


def detect_side(lha, rha, t):
    if abs(90 - lha) < t and abs(180 - rha) < t:
        return "l"
    elif abs(180 - lha) < t and abs(90 - rha) < t:
        return "r"
    return "n"


def detect_pose(lka, rka, lha, rha):
    up_tol = 15
    down_tol = 20

    if all(abs(160 - a) < up_tol for a in [lka, rka, lha, rha]):
        return USER_POSE.UP.value

    if abs(90 - lka) < down_tol and abs(90 - rka) < down_tol:
        return USER_POSE.DOWN.value

    if lka < 65 or rka < 65:
        return USER_POSE.TOO_DEEP.value

    if (65 < lka < 160) and (65 < rka < 160):
        return USER_POSE.NOT_ENOUGH.value

    return USER_POSE.UNKNOWN.value
