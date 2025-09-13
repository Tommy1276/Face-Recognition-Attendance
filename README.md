Face Recognition Attendance System
Overview
A real-time attendance system using Python, OpenCV, and the face_recognition library. This system automatically detects and marks attendance of individuals using face recognition. New faces can be added dynamically, and attendance is stored in CSV format.
Features
Real-time face detection and recognition
Face encoding and comparison for accurate recognition
Dynamic addition of new faces
Attendance logged in CSV with Name, Time, and Date
Live display panel of attendees and total count
Tkinter dialogs for user input and safe webcam exit
Image preprocessing and resizing for faster recognition
Scalable for schools, offices, or organizations


🔹 Installation
Clone the repository:
git clone https://github.com/YourUsername/Face-Recognition-Attendance.git
Navigate into the project folder:
cd Face-Recognition-Attendance
Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
Install dependencies:
pip install -r requirements.txt
🔹 Usage
Add known images to the Images_Attendance folder.
Run the project:
python AttendanceProject.py
When a new face is detected:
Enter a name to save it.
Click Cancel to skip.
Attendance is automatically stored in Attendance.csv.
🔹 Technologies Used
Python 3.12
OpenCV 4.x
face_recognition 1.3.0
NumPy
Tkinter
CSV
🔹 Notes
Ensure a working webcam is connected.
Large numbers of images may affect performance.
For best results, provide clear images of faces.
