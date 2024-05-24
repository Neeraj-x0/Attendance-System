from tkinter import *
from tkinter import ttk
from Register import Register
from Face_rec import FaceScan
from database import get_attendance_data

class Attendance(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Attendance System")
        self.pack(padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        self.lbl = Label(self, text="Welcome to Attendance System", font=("Arial", 16))
        self.lbl.pack(pady=(0, 20))

        # Register New Face Button
        self.btn_register = ttk.Button(self, text="Register New Face", command=self.register_face)
        self.btn_register.pack(fill='x', pady=(0, 10))

        # Scan for Faces Button
        self.btn_scan = ttk.Button(self, text="Scan for Faces", command=self.scan_faces)
        self.btn_scan.pack(fill='x')

        self.btn_show = ttk.Button(self, text="Show Attendance", command=self.show_attendance)
        self.btn_show.pack(fill='x')

        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Show Attendance", command=self.show_attendance)

    def register_face(self):
        self.newWindow = Toplevel(self.master)
        self.app = Register(self.newWindow)

    def scan_faces(self):
        self.newWindow = Toplevel(self.master)
        self.app = FaceScan(self.newWindow)  # Assuming ScanFace function directly opens a window for face scanning

    def show_attendance(self):
        # Fetch attendance data from the database
        attendance_data = get_attendance_data()

        # Create a new window to display attendance
        self.attendance_window = Toplevel(self.master)
        self.attendance_window.title("Attendance Details")

        # Create a text widget to display attendance details
        self.text_widget = Text(self.attendance_window, wrap=WORD)
        self.text_widget.pack(expand=True, fill=BOTH, padx=10, pady=10)

        # Insert attendance data into the text widget
        for record in attendance_data:
            name, student_id, timestamp = record
            self.text_widget.insert(END, f"Name: {name}\nStudent ID: {student_id}\nTime: {timestamp}\n\n")

def main():
    root = Tk()
    app = Attendance(root)
    app.mainloop()

if __name__ == "__main__":
    main()
