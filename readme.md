
# Exam Authentication App

This is a simple Python application for exam authentication using webcam and face recognition.

## Installation

1. Make sure you have Python installed on your system. You can download it from [here](https://www.python.org/downloads/).

2. Clone this repository to your local machine:
   ```
   git clone https://github.com/Yosri-zayani/ExamAuthApp
   ```

3. Navigate to the project directory:
   ```
   cd exam-authentication-app
   ```

4. Install the required Python libraries using pip:
   ```
   pip install -r requirements.txt
   ```

## Launching the Application

1. Once you have installed the required libraries, you can launch the application by running `main.py`:
   ```
   python main.py
   ```

2. The application window will open, displaying the webcam feed.

## Customization

1. **Database Path**: You can change the path to the database of images in the `db_path` variable in `main.py`. This database should contain images of users for face recognition.

2. **Relative Paths**: Make sure to adjust any relative paths in the code according to your directory structure.

## Usage

1. When the application is running, click the "Capture" button to capture the current frame from the webcam.

2. The application will perform face recognition on the captured frame and check if the face matches any user in the database.

3. If a match is found, the application will display a welcome message with the user's name.

4. If no match is found, the application will display a message indicating that the user is not recognized.

5. Close the application window to exit.
