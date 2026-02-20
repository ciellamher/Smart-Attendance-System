import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime # NEW: Imports the time and date library

# --- STEP 1: ENCODINGS ---
path = 'student_images'
images = []
classNames = []
myList = os.listdir(path)
myList = [f for f in myList if not f.startswith('.')]

print(f'Found {len(myList)} image(s). Encoding faces...')

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0]) 

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# --- NEW STEP: ATTENDANCE LOGGING FUNCTION ---
def markAttendance(name):
    # Automatically get today's date (e.g., "Feb_20_2026")
    today_date = datetime.now().strftime('%b_%d_%Y')
    filename = f'Attendance_{today_date}.csv'
    
    # If the file for today doesn't exist yet, create it and write the headers
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            f.write('Name,Time\n')
            
    # Open the file to read who is already logged today
    with open(filename, 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0]) # Grab just the names
            
        # If the person's name is NOT in the list, log them!
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S') # Get exact time (e.g., 14:30:05)
            f.write(f'{name},{dtString}\n')
            print(f"Logged {name} at {dtString}") # Prints to your VS Code terminal

# ---------------------------------------------

encodeListKnown = findEncodings(images)
print('Encoding Complete! Starting Webcam...')

# --- STEP 2: LIVE TEST ---
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4 
            
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
            # CALL THE NEW FUNCTION HERE
            markAttendance(name)

    cv2.imshow('Face Recognition Test', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()