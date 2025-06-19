import numpy as np


# EUCLIDEAN DISTANCE BETWEEN TWO POINTS
def distance(pt1, pt2):
    return np.linalg.norm(pt2 - pt1)


# Detect if the driver is looking away
def gaze_direction(face_landmarks):
    left_eye = face_landmarks[36:42]  # Left eye landmarks
    right_eye = face_landmarks[42:48]  # Right eye landmarks
    nose = face_landmarks[30]  # Nose landmark

    left_eye_center_x = np.mean([point[0] for point in left_eye])
    right_eye_center_x = np.mean([point[0] for point in right_eye])

    nose_to_left_eye_dist = abs(nose[0] - left_eye_center_x)
    nose_to_right_eye_dist = abs(nose[0] - right_eye_center_x)

    gaze_threshold = (right_eye_center_x - left_eye_center_x) * 0.35

    if nose_to_left_eye_dist > gaze_threshold > nose_to_right_eye_dist:
        return -1
    elif nose_to_right_eye_dist > gaze_threshold > nose_to_left_eye_dist:
        return 1
    else:
        return 0


# CALCULATE EAR -- Eye aspect ratio
def blinked(a, b, c, d, e, f):
    up = distance(b, d) + distance(c, e)
    down = distance(a, f)
    rate = up / (2.0 * down)
    if rate > 0.25:
        return 2
    elif 0.15 < rate <= 0.25:
        return 1
    else:
        return 0
