# 📸 Smart Attendance Face Recognition System

A real-time, lightweight facial recognition attendance system built with Python and OpenCV. This project captures video from a webcam, identifies registered individuals using 128-dimensional facial encodings, and automatically logs their attendance with timestamps into a daily CSV file.

## ✨ Features
* **Real-Time Recognition:** Processes live webcam feeds to detect and identify faces instantly.
* **Automated Logging:** Automatically generates a daily `.csv` file (e.g., `Attendance_Feb_20_2026.csv`) and logs the exact time of arrival.
* **Duplicate Prevention:** Ensures an individual is only logged once per day.
* **Privacy Focused:** Raw images and attendance logs are kept strictly local and ignored by Git.

## 🛠️ Tech Stack
* **Language:** Python 3.11
* **Computer Vision:** `opencv-python`
* **Facial Recognition Engine:** `face_recognition` (dlib-based)
* **Data Processing:** `numpy`

## 🚀 How to Run (Local Setup)
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ciellamher/Smart-Attendance-System.git](https://github.com/ciellamher/Smart-Attendance-System.git)