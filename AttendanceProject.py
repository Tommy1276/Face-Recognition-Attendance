# Face Recognition Attendance System - Full Modified Version
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from tkinter import Tk, simpledialog

# Hide main Tkinter window
root = Tk()
root.withdraw()

# Path for known images
path = 'Images_Attendance'
images = []
classNames = []

# Load known images
myList = os.listdir(path)
print("[INFO] Found images:", myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0].upper())
print("[INFO] Class Names:", classNames)

# Encode faces
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes:
            encodeList.append(encodes[0])
    return encodeList

# Mark attendance
def markAttendance(name):
    filename = 'Attendance.csv'
    with open(filename, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            time_now = datetime.now()
            tString = time_now.strftime('%H:%M:%S')
            dString = time_now.strftime('%d/%m/%Y')
            f.writelines(f'{name},{tString},{dString}\n')
            return tString
    return None

encodeListKnown = findEncodings(images)
print("[INFO] Encoding Complete")

cap = cv2.VideoCapture(0)

present_names = set()
last_marked_time = {}

while True:
    success, img = cap.read()
    if not success:
        print("[ERROR] Could not access webcam.")
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    new_detected_names = []

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        if True in matches:
            matchIndex = np.argmin(faceDis)
            name = classNames[matchIndex]
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            if name not in present_names:
                time_stamp = markAttendance(name)
                if time_stamp:
                    present_names.add(name)
                    last_marked_time[name] = time_stamp
                    new_detected_names.append(name)

        else:
            # New face detected
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            new_face_img = img[y1:y2, x1:x2]

            cv2.imshow('New Face Detected', new_face_img)
            cv2.waitKey(1)

            # Ask user for name
            new_name = simpledialog.askstring("New Face Detected",
                                              "Enter name to save (or Cancel to skip):")
            if new_name:  # Only add if user enters a name
                save_path = f'Images_Attendance/{new_name}.jpg'
                cv2.imwrite(save_path, new_face_img)
                print(f"[INFO] Saved new face as {save_path}")

                classNames.append(new_name.upper())
                encodeListKnown.append(face_recognition.face_encodings(new_face_img)[0])
                print(f"[INFO] Updated known faces with {new_name.upper()}")
            else:
                print("[INFO] New face skipped.")

    # Attendance panel with dynamic spacing
    panel_x, panel_y = 10, 10
    dy = 30
    cv2.rectangle(img, (panel_x-5, panel_y-5),
                  (panel_x+500, panel_y + (len(present_names)+3)*dy), (50,50,50), cv2.FILLED)
    cv2.putText(img, "Attendance List:", (panel_x, panel_y + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

    for i, name in enumerate(sorted(present_names)):
        y = panel_y + (i+1)*dy
        info_text = f"{name} | {last_marked_time.get(name,'')}"
        cv2.putText(img, info_text, (panel_x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    # Total count below attendance list
    cv2.putText(img, f"Total Present: {len(present_names)}", 
                (panel_x, panel_y + (len(present_names)+1)*dy + 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,200,255), 2)

    if new_detected_names:
        notif_text = f"Marked: {', '.join(new_detected_names)}"
        cv2.putText(img, notif_text, (panel_x, panel_y + (len(present_names)+2)*dy + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

    cv2.imshow('Webcam', img)

    # ✅ Reliable Quit: Press 'q' to exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("[INFO] Quitting...")
        break

cap.release()
cv2.destroyAllWindows()
