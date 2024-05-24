import face_recognition
from tkinter import messagebox
import cv2
import os
from datetime import datetime
from database import save_face_data

video_capture = 0

class FaceScan:
    def __init__(self, master):
        self.master = master
        self.master.title("Face Scanner")
        ScanFace()
        self.master.destroy()
idname = {}         
# Load images from the "images" folder and generate face encodings
def load_known_faces(image_folder):
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(image_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            name = os.path.splitext(filename)[0]
            image_path = os.path.join(image_folder, filename)
            image = face_recognition.load_image_file(image_path)
            # Get face encodings only if a face is detected
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                known_face_encodings.append(face_encodings[0])
                known_face_names.append(name.split("_")[0])
                idname[name.split("_")[0]] = name.split("_")[1]

    return known_face_encodings, known_face_names


# Function to save detected face data to a JSON file


# Function to scan for faces using webcam
def ScanFace():
    video_capture = cv2.VideoCapture(0)
    # Initialize video capture from webcam
    

    # Load known faces and their encodings
    image_folder = "images"
    known_face_encodings, known_face_names = load_known_faces(image_folder)

    # Initialize variables
    process_this_frame = True

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(small_frame)
            face_encodings = face_recognition.face_encodings(small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                    # Save detected face data to a JSON file
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    face_data = {"name": name, "time": timestamp,"student_id":idname[name]}
                    isaved = save_face_data(face_data)
                    if isaved:
                        messagebox.showinfo("Face Recognition", f"Attendance marked for {name}")   
                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Draw a label with a name below the face
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom + 30), font, 1.0, (0, 255, 0), 1)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q') or ord('Q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


