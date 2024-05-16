import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from face_recognition import FaceRecognition

class WebcamApp:
    def __init__(self, window, window_title, db_path):
        self.window = window
        self.window.title(window_title)

        # Set the background image
        self.bg_image = Image.open("background.jpg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(window, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Title label
        self.title_label = ttk.Label(window, text="ExamAuthApp", font=("Helvetica", 28, "bold"),  foreground='Black')
        self.title_label.pack(pady=10)

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        # Set desired width and height for the video frame
        self.frame_width = 320  # Set desired width
        self.frame_height = 240  # Set desired height
        self.canvas = tk.Canvas(window, width=self.frame_width, height=self.frame_height, background='pink')
        self.canvas.pack()

        self.db_path = db_path

        self.btn_capture = ttk.Button(window, text="Capture", command=self.capture)
        self.btn_capture.pack(pady=10)

        self.match_label = ttk.Label(window, text="", font=("Helvetica", 20),  foreground='Black')
        self.match_label.pack(pady=10)

        self.delay = 10
        self.update()

    def capture(self):
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite("captured_frame.jpg", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.check_match("captured_frame.jpg", frame)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.resize(frame, (self.frame_width, self.frame_height))  # Resize the frame to the desired dimensions
            # Detect faces in the frame
            faces = self.detect_faces(frame)
            if faces is not None:
                # Draw a rectangle around each face
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Convert the frame to an image and display it
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)

    def detect_faces(self, frame):
        # Load the pre-trained face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces

    def check_match(self, img_path, frame):
        face_recognition = FaceRecognition()
        try:
            match_found, filename_before_dot = face_recognition.check_match(img_path, self.db_path)
            if match_found:
                self.match_label.config(text=f"Welcome to the exam, {filename_before_dot}")
            else:
                self.match_label.config(text="No match found in database. This user is not a student")
        except Exception as e:
            print("Error:", e)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
