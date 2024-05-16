import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace

class WebcamApp:
    def __init__(self, window, window_title, db_path):
        self.window = window
        self.window.title(window_title)

        # Title label
        self.title_label = ttk.Label(window, text="ExamAuthApp", font=("Helvetica", 20, "bold"))
        self.title_label.pack()

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.frame_width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas = tk.Canvas(window, width=self.frame_width, height=self.frame_height)
        self.canvas.pack()

        self.db_path = db_path

        self.btn_capture = ttk.Button(window, text="Capture", command=self.capture)
        self.btn_capture.pack(pady=10)

        self.match_label = ttk.Label(window, text="", font=("Helvetica", 14))
        self.match_label.pack()

        self.delay = 10
        self.update()

        # Make the app fullscreen
        self.window.attributes("-fullscreen", True)

        self.window.mainloop()

    def capture(self):
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite("captured_frame.jpg", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.check_match("captured_frame.jpg", frame)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
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
        try:
            dfs = DeepFace.find(img_path=img_path, db_path=self.db_path)
            match_found = any(len(df['distance']) > 0 for df in dfs)
            if match_found:
                filename = dfs[0].iloc[0]['identity']
                # Split after '\' and then extract substring before ".jpeg"
                filename_parts = filename.split('\\')
                filename_before_dot = filename_parts[-1].split(".jpg")[0]
                self.match_label.config(text=f"Welcome to the exam, {filename_before_dot}")
            else:
                self.match_label.config(text="No match found in database. This user is not a student")
        except Exception as e:
            print("Error:", e)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__ == "__main__":
    db_path = "C:/Users/Zayen/OneDrive/Desktop/Face_recognition_mediapip/users"  # Change this to your database path
    root = tk.Tk()
    root.geometry("500x400")  # Set window size
    app = WebcamApp(root, "Exam Authentication App", db_path)
