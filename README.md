# Driver-drowsiness-detection


![drowsiness](https://github.com/user-attachments/assets/c0441227-52f2-4a5c-b630-a670b0674f82)

Driver drowsiness is a major cause of road accidents, making the need for safety solutions crucial. A driver drowsiness detection system addresses this by monitoring the driver's alertness in real-time. Using sensors and machine learning, it analyzes eye movements, blinking, and head position to detect signs of fatigue. When drowsiness is detected, the system alerts the driver, helping to prevent accidents. This technology enhances road safety and is increasingly integrated into modern vehicles to ensure safer driving conditions.
Opencv. dlib and shape_predictor_68_face_landmarks.dat (you can download it) are used in this project

The python dlib library is used to detect the face and also the face's shape (68 face landmarks) and OpenCv is used to apply several manipulations on the image
After the face is detected the Eue Aspect Ratio is calculated and using this value the program will decide either the driver is sleepy or not.
If the driver is sleeping an alarm sound will be played on another thread to avoid collision with the main thread.


Please check the images bellow!

![ear](https://github.com/user-attachments/assets/99399897-fd3a-4923-bbe1-296cbb7d3f49)


![active](https://github.com/user-attachments/assets/9e765e01-37a0-492c-9451-4178ae6414e6)


![drowsy](https://github.com/user-attachments/assets/4beeee19-1d9c-4bcb-8c44-5690d54ce841)


![sleeping](https://github.com/user-attachments/assets/aec8970b-d2b3-43e7-997a-bffb9f78cadb)
