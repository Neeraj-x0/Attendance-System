import cv2
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog  # Importing simpledialog submodule
from PIL import Image, ImageTk
class Register:
    def __init__(self, master):
        self.master = master
        self.master.title("Camera App")

        # Create a label to display the camera preview
        self.preview_label = tk.Label(master)
        self.preview_label.pack()

        # Create a Capture button
        self.capture_button = tk.Button(
            master, text="Capture", command=self.capture_photo
        )
        self.capture_button.pack(pady=10)

        # Initialize video capture from webcam
        self.video_capture = cv2.VideoCapture(0)

        # Start the update loop
        self.update_preview()

    def update_preview(self):
        # Capture frame-by-frame
        ret, frame = self.video_capture.read()

        if ret:
            # Convert the frame from BGR color to RGB color
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize the frame to fit the label
            height, width, _ = rgb_frame.shape
            new_width = min(width, 800)
            new_height = int((height / width) * new_width)
            resized_frame = cv2.resize(rgb_frame, (new_width, new_height))

            # Convert the frame to a Tkinter-compatible image
            img = Image.fromarray(resized_frame)
            imgtk = ImageTk.PhotoImage(image=img)

            # Update the preview label with the new image
            self.preview_label.imgtk = imgtk
            self.preview_label.config(image=imgtk)

        # Schedule the next update after 10 milliseconds
        self.master.after(10, self.update_preview)

    def capture_photo(self):
        # Ask for name and admission number
        ret, frame = self.video_capture.read()
        name = simpledialog.askstring("Input", "Enter your name:")
        if not name:
            return

        admission_number = simpledialog.askstring(
            "Input", "Enter your admission number:"
        )
        if not admission_number:
            return

        # Define the path to the "images" folder
        image_folder = "images"

        # Create the "images" folder if it doesn't exist
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        # Define the filename for the photo
        filename = f"{name}_{admission_number}.jpg"
        file_path = os.path.join(image_folder, filename)

        # Capture frame-by-frame
        

        if ret:
            # Save the captured photo
            cv2.imwrite(file_path, frame)
            messagebox.showinfo("Success", f"Photo captured and saved as {filename}")
        else:
            messagebox.showerror("Error", "Failed to capture photo")
        self.video_capture.release()
        cv2.destroyAllWindows()
        
        self.master.destroy()


