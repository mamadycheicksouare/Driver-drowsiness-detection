# Driver-drowsiness-detection
Driver drowsiness and distraction are among the leading causes of car accidents worldwide. In this project, I developed a driver drowsiness and distraction detection system using Python, OpenCV, Dlib, and YOLO.

A yolo (yolo11n-cls.pt) model was trained to classify the driver's facial region as either drowsy or non-drowsy. The original dataset, which was formatted for object detection, was converted into a classification dataset using the detectiondataset_to_classificationdataset.py script.





![drowsy_detected](https://github.com/user-attachments/assets/60515727-604b-4c19-99a1-a7ac21733071)




![non-drowsy_detected](https://github.com/user-attachments/assets/ea1b49c1-3ee5-4f8f-a0a0-90b3c442443f)



Drowsiness is detected through a combination of a YOLO model and various computer vision techniques by analyzing eye movements and eye closure using Eye Aspect Ratio (EAR) metrics.

Distraction is detected by analyzing the position of the driver's head. This is done by measuring the distance between the nose and the eyes to determine whether the driver is looking to the left or right.



![green](https://github.com/user-attachments/assets/2a6eb0fb-8604-4aac-b758-7cf1dbad8583)



![red](https://github.com/user-attachments/assets/14400604-a92d-44f5-849b-f9dbdfd19e7b)











