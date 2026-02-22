# 📸 Smart Attendance Face Recognition System

An advanced, real-time facial recognition attendance system built with Python and OpenCV. This project captures video from a webcam, identifies students using 128-dimensional facial encodings, and features Voice AI feedback, smart surname logic, and dynamic CSV database management.

## ✨ Key Features
* **Real-Time Recognition:** Processes live webcam feeds to detect and identify faces instantly.
* **Dynamic CSV Database:** Automatically generates and reads from a `students.csv` file. Professors can easily add or remove students by editing the spreadsheet without touching the code.
* **Smart Naming Engine:** Uses a university-standard surname basis (e.g., "JIMENEZ"). Automatically detects duplicate surnames and applies first initials (e.g., "JIMENEZ, G").
* **Voice AI & Audio Feedback:** Uses macOS native audio to play a success "Ping" and speak the student's name out loud upon logging. Unknown faces trigger a warning beep and an "unrecognized" voice prompt.
* **Automated Logging & Duplicate Prevention:** Generates a daily `.csv` file (e.g., `Attendance_Feb_23_2026.csv`) logging the exact time of arrival, preventing multiple entries for the same student in a single day.
* **Privacy Focused:** Raw student images and daily attendance logs are kept strictly local.

## 🛠️ Tech Stack
* **Language:** Python 3.11
* **Computer Vision:** `opencv-python`
* **Facial Recognition Engine:** `face_recognition` (dlib-based)
* **Data Processing:** `numpy`, `csv`, `datetime`

## 🚀 How to Run (Local Setup)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ciellamher/Smart-Attendance-System.git](https://github.com/ciellamher/Smart-Attendance-System.git)
   cd Smart-Attendance-System