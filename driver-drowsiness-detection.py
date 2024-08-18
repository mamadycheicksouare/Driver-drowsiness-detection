import cv2
import numpy as np
import dlib
from imutils import face_utils
import pygame
import threading

# Initialize pygame mixer
pygame.mixer.init()

#  GET VIDEO FROM THE WEBCAM
video = cv2.VideoCapture(0)

# FACE DETECTION FUNCTION
detector = dlib.get_frontal_face_detector()

# DETECT 68 FACE LANDMARKS
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

sleep = 0
drowsy = 0
active = 0
status = ""
color = (0, 0, 0)


# EUCLIDEAN DISTANCE BETWEEN TWO POINTS
def distance(pt1, pt2):
    dist = np.linalg.norm(pt2 - pt1)
    return dist


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


def play_alarm():
    pygame.mixer.music.load('alarm.mp3')
    pygame.mixer.music.play()


cv2.namedWindow("Driver drowsiness detection", cv2.WINDOW_NORMAL)

while True:
    state, frame = video.read()

    if not state:  # Check if the webcam feed is available
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

        landmarks = face_utils.shape_to_np(predictor(gray, face))

        # CALCULATE EAR FOR BOTH LEFT AND RIGHT EYES
        left = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        if left == 0 or right == 0:
            sleep += 1
            drowsy = 0
            active = 0

            if sleep > 8:
                status = "SLEEPING"
                color = (0, 0, 255)
                threading.Thread(target=play_alarm).start()

        elif left == 1 or right == 1:
            sleep = 0
            active = 0
            drowsy += 1

            if drowsy > 5:
                status = "DROWSY"
                color = (255, 0, 0)

        else:
            drowsy = 0
            sleep = 0
            active += 1

            if active > 5:
                status = "ACTIVE"
                color = (0, 255, 0)

        # SHOW MESSAGE
        cv2.putText(frame, status, (80, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        for n in range(0, 68):
            (x, y) = landmarks[n]
            cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)

        cv2.imshow("Driver drowsiness detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()
