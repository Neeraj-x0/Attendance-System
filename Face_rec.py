import face_recognition
from tkinter import messagebox, Tk
import cv2
import os
from datetime import datetime
from database import save_face_data

class FaceScan:
    def __init__(self, master=None):
        self.master = master or Tk()
        self.master.title("Face Scanner")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.video_capture = cv2.VideoCapture(0)
        self.known_face_encodings, self.known_face_names, self.idname = self.load_known_faces("images")
        self.process_this_frame = True
        self.scan_face()
        self.master.mainloop()

    def on_closing(self):
        self.video_capture.release()
        cv2.destroyAllWindows()
        self.master.destroy()

    def load_known_faces(self, image_folder):
        known_face_encodings = []
        known_face_names = []
        idname = {}

        for filename in os.listdir(image_folder):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                name = os.path.splitext(filename)[0]
                image_path = os.path.join(image_folder, filename)
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)
                if face_encodings:
                    known_face_encodings.append(face_encodings[0])
                    known_face_names.append(name.split("_")[0])
                    idname[name.split("_")[0]] = name.split("_")[1]

        return known_face_encodings, known_face_names, idname

    def scan_face(self):
        while True:
            ret, frame = self.video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            if self.process_this_frame:
                face_locations = face_recognition.face_locations(small_frame)
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)
                face_names = []

                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"

                    if True in matches:
                        first_match_index = matches.index(True)
                        name = self.known_face_names[first_match_index]
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        face_data = {"name": name, "time": timestamp, "student_id": self.idname[name]}
                        if save_face_data(face_data):
                            messagebox.showinfo("Face Recognition", f"Attendance marked for {name}")

                    face_names.append(name)

            self.process_this_frame = not self.process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom + 30), font, 1.0, (0, 255, 0), 1)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    FaceScan()