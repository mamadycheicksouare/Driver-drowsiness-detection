
from detection import classify_face
from audio import play_alarm, stop_alarm
from face import blinked, gaze_direction
import cv2
import dlib
from imutils import face_utils
import threading



# GET VIDEO FROM THE WEBCAM
video = cv2.VideoCapture(0)

# FACE DETECTION FUNCTION
detector = dlib.get_frontal_face_detector()

# DETECT 68 FACE LANDMARKS
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Variables to track drowsiness and gaze
sleep = 0
drowsy = 0
yolo_detection = 0
active = 0
no_face = 0
warning_head = 0
alarm_playing = False

status = ""
color = (0, 0, 0)
warning_color = (0, 0, 255)

head_position = {-1:"Looking Left", 1:"Looking Right", 0:"Normal "}



cv2.namedWindow("Driver drowsiness detection", cv2.WINDOW_NORMAL)

while True:
    state, frame = video.read()

    if not state:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) == 0:
        no_face += 1
        if no_face > 20 and alarm_playing:  # No face detected for too long
            stop_alarm()
        continue

    no_face = 0  # Reset no_face counter when a face is detected

    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        landmarks = face_utils.shape_to_np(predictor(gray, face))

        face_crop = frame[y1:y2, x1:x2]

        yolo_detection = classify_face(face_crop)


        # Detect gaze direction
        gaze = gaze_direction(landmarks)
        if gaze != 0:
            warning_head += 1
            if warning_head > 15 and not alarm_playing:
                threading.Thread(target=play_alarm).start()
                warning_color = (0, 0, 255)
        else:
            warning_head = 0
            warning_color = (0, 255, 0)

        # Calculate EAR for both left and right eyes
        left = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        # Drowsiness detection logic
        if (left == 0 or right == 0) or yolo_detection == 1:  # Sleeping
            sleep += 1
            drowsy = 0
            active = 0

            if sleep > 5 and not alarm_playing:
                status = "Sleeping"
                print(yolo_detection)
                color = (0, 0, 255)
                threading.Thread(target=play_alarm).start()

        elif (left == 1 or right == 1) or yolo_detection == 1:  # Drowsy
            sleep = 0
            active = 0
            drowsy += 1

            if drowsy > 5 :
                status = "Drowsy"
                color = (255, 0, 0)
                print(yolo_detection)
                if alarm_playing:
                    stop_alarm()

        else:  # Active
            sleep = 0
            drowsy = 0
            active += 1

            if active > 5:
                status = "Active"
                color = (0, 255, 0)
                if alarm_playing:
                    stop_alarm()

        # Display information on the frame

        cv2.putText(frame, "Drowsiness:" + status, (70, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(frame, "Head position:" + head_position[gaze], (70, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, warning_color, 2)

        for n in range(0, 68):
            (x, y) = landmarks[n]
            cv2.circle(frame, (x, y), 1, warning_color, -1)

    cv2.imshow("Driver drowsiness detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
stop_alarm()
