import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Student Face Attendance System")

today_date = datetime.now().strftime("%Y-%m-%d")

known_face_encodings = []
known_face_names = []

students = [
    ("136.jpeg", "Sandesh - 2111CS020136"),
    ("133.jpg", "Ganapathi - 2111CS020133")
]

for image_path, name in students:
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)
    known_face_names.append(name)

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
detected_faces = set() 
video_capture = None
year = ""
section = ""

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480

def start_attendance():
    global year, section
    year = simpledialog.askstring("Input", "Enter the Year:")
    if year is None:  # If user cancels
        return
    section = simpledialog.askstring("Input", "Enter the Section:")
    if section is None:  # If user cancels
        return
    start_video_capture()

def start_video_capture():
    global video_capture
    video_capture = cv2.VideoCapture(0)
    start_button.pack_forget()
    options_button.pack_forget()
    exit_button.pack_forget()
    detect_faces()
    stop_button.pack(pady=10)

def detect_faces():
    global process_this_frame, face_locations, face_encodings, face_names
    ret, frame = video_capture.read()
    if not ret:
        messagebox.showerror("Error", "Failed to capture video")
        return

    # Resize the frame to fixed size
    frame = cv2.resize(frame, (VIDEO_WIDTH, VIDEO_HEIGHT))

    if process_this_frame:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                detected_faces.add(name)

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)
    video_label.after(10, detect_faces)

def stop_video_capture():
    global video_capture
    if video_capture is not None:
        video_capture.release()
        video_capture = None
        cv2.destroyAllWindows()
        stop_button.pack_forget()
        save_attendance()

def save_attendance():
    global year, section
    filename_presentees = f"Presentees - {year}-{section} - {today_date}.csv"
    filename_absentees = f"Absentees - {year}-{section} - {today_date}.csv"
    
    with open(filename_presentees, mode='w', newline='') as presentees_file:
        presentees_writer = csv.writer(presentees_file)
        presentees_writer.writerow(['Detected Faces'])
        for face in detected_faces:
            presentees_writer.writerow([face])

    with open(filename_absentees, mode='w', newline='') as absentees_file:
        absentees_writer = csv.writer(absentees_file)
        absentees_writer.writerow(['Absentees'])
        for face in known_face_names:
            if face not in detected_faces:
                absentees_writer.writerow([face])

    messagebox.showinfo("Attendance Saved", f"Attendance has been saved for {today_date}")

def open_options():
    messagebox.showinfo("Options", "Options screen placeholder")

def exit_program():
    root.quit()

# GUI Layout
main_title = tk.Label(root, text="Welcome to Malla Reddy University", font=("Helvetica", 16))
main_title.pack(pady=20)

start_button = tk.Button(root, text="Start", command=start_attendance, width=20)
start_button.pack(pady=10)

options_button = tk.Button(root, text="Options", command=open_options, width=20)
options_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_program, width=20)
exit_button.pack(pady=10)

video_label = tk.Label(root)
video_label.pack()

stop_button = tk.Button(root, text="Stop Attendance", command=stop_video_capture, width=20)

root.mainloop()