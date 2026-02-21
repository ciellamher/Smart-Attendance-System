import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import time
import csv # NEW: To read the professor's database file

# ==========================================
# ⚙️ SESSION SETTINGS
# ==========================================
CURRENT_SUBJECT = "Intelligent Systems 101"
PROFESSOR_NAME = "Prof. Dela Cruz"

# ==========================================
# 🗂️ DYNAMIC STUDENT DATABASE LOAD
# ==========================================
db_file = 'students.csv'
STUDENT_DB = {}

# 1. If the professor's database doesn't exist, auto-create a template!
if not os.path.isfile(db_file):
    with open(db_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Image_Name', 'Full_Name', 'Course', 'Section'])
        writer.writerow(['GRACIELLA', 'Graciella M. Jimenez', 'BS Computer Science', 'CS-3A'])
    print(f"Created new database template: {db_file}")

# 2. Read the database file into our system
with open(db_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        img_name = row["Image_Name"].upper()
        STUDENT_DB[img_name] = {
            "full_name": row["Full_Name"],
            "course": row["Course"],
            "section": row["Section"]
        }

# --- SMART NAMING ENGINE ---
display_names = {}
surname_counts = {}

for key, info in STUDENT_DB.items():
    surname = info["full_name"].split()[-1].upper() 
    surname_counts[surname] = surname_counts.get(surname, 0) + 1

for key, info in STUDENT_DB.items():
    parts = info["full_name"].split()
    first_name = parts[0].upper()
    surname = parts[-1].upper()
    
    if surname_counts[surname] > 1:
        display_names[key] = f"{surname}, {first_name[0]}" 
    else:
        display_names[key] = surname 

# ==========================================

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

# --- ATTENDANCE LOGGING ---
def markAttendance(raw_key):
    today_date = datetime.now().strftime('%b_%d_%Y')
    filename = f'Attendance_{today_date}.csv'
    
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            f.write('Full Name,Course,Section,Subject,Professor,Time,Status\n')
            
    with open(filename, 'r+') as f:
        myDataList = f.readlines()
        logged_names = [line.split(',')[0] for line in myDataList]
        
        student_info = STUDENT_DB.get(raw_key, {"full_name": raw_key, "course": "N/A", "section": "N/A"})
        full_name = student_info["full_name"]
        
        if full_name not in logged_names:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            
            course = student_info["course"]
            section = student_info["section"]
            status = "Present" 
            
            f.write(f'{full_name},{course},{section},{CURRENT_SUBJECT},{PROFESSOR_NAME},{dtString},{status}\n')
            print(f"Logged {full_name} for {CURRENT_SUBJECT}")
            
            return True 
            
    return False 

# ---------------------------------------------

encodeListKnown = findEncodings(images)
print('Encoding Complete! Starting Webcam...')

# --- STEP 2: LIVE TEST WITH BEEP & SMART VOICE ---
cap = cv2.VideoCapture(0)
last_unknown_time = 0 

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

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4 

        if faceDis[matchIndex] < 0.50:
            raw_key = classNames[matchIndex].upper()
            display_name = display_names.get(raw_key, raw_key)
            
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, display_name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
            is_new_entry = markAttendance(raw_key)
            
            if is_new_entry:
                speak_name = display_name.replace(",", "")
                os.system(f"(afplay /System/Library/Sounds/Ping.aiff && say '{speak_name}, Present. Next.') &") 
                
        else:
            name = "UNKNOWN"
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
            current_time = time.time()
            if current_time - last_unknown_time > 5:
                os.system("(afplay /System/Library/Sounds/Basso.aiff && say 'Unrecognized, not from this class. Next.') &")
                last_unknown_time = current_time

    cv2.imshow('Smart Attendance System', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()