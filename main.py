import tkinter as tk
from tkinter import ttk
from webcam import WebcamApp

if __name__ == "__main__":
    db_path = "C:/Users/Zayen/OneDrive/Desktop/Face_recognition_mediapip/users"  # Change this to your database path
    root = tk.Tk()
    root.geometry("800x600")  # Set window size
    app = WebcamApp(root, "Exam Authentication App", db_path)
    root.mainloop()
