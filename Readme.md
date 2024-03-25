# Face Recognition Attendance System

## Description:

This project is a Face Recognition Attendance System developed using Python, emphasizing Object-Oriented Programming (OOP) concepts. It integrates face_recognition library for face detection and recognition, tkinter for GUI components, and OpenCV for capturing video frames. The system operates by scanning faces in real-time using the webcam, matching them with known faces, and marking attendance based on recognized faces.

## Files:

1. FaceScan.py - Contains the main program code for face scanning and attendance marking, implemented with OOP principles.
2. Register.py - Module for registering new faces by capturing photos using the webcam, designed with OOP concepts.
3. Face_rec.py - Module for face recognition functionalities, organized with OOP methodology.
4. images/ - Directory containing images of known faces for recognition.
5. face_data.json - JSON file for storing attendance data.

## Usage:
To run the Face Recognition Attendance System:
    1. Execute the FaceScan.py file using Python.
    2. Ensure that the 'images' folder contains images of known faces for recognition.
    3. The system will begin scanning for faces using the connected webcam.
    4. Recognized faces will be marked for attendance, and the details will be stored in the 'face_data.json' file.
    5. Press 'q' on the keyboard to quit the application.

## Dependencies:
1. Python 3.x
2. face_recognition library
3. tkinter library
4. OpenCV (cv2) library
5. PIL (Pillow) library

## Notes:
- Ensure that the webcam is connected and properly configured.
- Adequate lighting is essential for accurate face recognition.
- You can improve recognition accuracy by adding more images of known faces to the 'images' folder.
- Handle any exceptions that may occur during face recognition or file operations for robust performance.
- Emphasizing the usage of OOP concepts, the project is structured with modular components, promoting code reusability, encapsulation, and maintainability.
