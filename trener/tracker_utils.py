from detection_utils import calculate_angle, USER_POSE


def get_body_points(lm):
    def p(idx):
        return [lm[idx].x, lm[idx].y]

    return {
        "l_sh": p(11),
        "r_sh": p(12),
        "l_hip": p(23),
        "r_hip": p(24),
        "l_knee": p(25),
        "r_knee": p(26),
        "l_ank": p(27),
        "r_ank": p(28),
        "l_ft": p(31),
        "r_ft": p(32),
    }


def get_all_angles(pts):
    return {
        "lka": calculate_angle(pts["l_hip"], pts["l_knee"], pts["l_ank"]),
        "rka": calculate_angle(pts["r_hip"], pts["r_knee"], pts["r_ank"]),
        "lha": calculate_angle(pts["l_sh"], pts["l_hip"], pts["l_knee"]),
        "rha": calculate_angle(pts["r_sh"], pts["r_hip"], pts["r_knee"]),
        "laa": calculate_angle(pts["l_knee"], pts["l_ank"], pts["l_ft"]),
        "raa": calculate_angle(pts["r_knee"], pts["r_ank"], pts["r_ft"]),
    }


def update_tracker(current_val, tracker, smooth_frames):
    if current_val == tracker["last"]:
        tracker["count"] += 1
    else:
        tracker["last"] = current_val
        tracker["count"] = 0

    if tracker["count"] >= smooth_frames:
        return current_val
    return None


def process_exercise_logic(pose, goal_reached, rep_counter):
    if pose == USER_POSE.DOWN.value:
        goal_reached = True
    if pose == USER_POSE.UP.value and goal_reached:
        rep_counter += 1
        goal_reached = False
    return goal_reached, rep_counter
