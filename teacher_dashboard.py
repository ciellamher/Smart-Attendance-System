import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import shutil
import os
import csv
import json
from datetime import datetime

# --- 1. STUDENT REGISTRATION FUNCTIONS ---
def upload_photo():
    filepath = filedialog.askopenfilename(title="Select Student Photo", filetypes=(("Image files", "*.jpg *.png *.jpeg"), ("All files", "*.*")))
    if filepath:
        photo_path_var.set(filepath)

def save_student():
    first_name = entry_first.get().strip()
    last_name = entry_last.get().strip()
    course = entry_course.get().strip()
    section = entry_section.get().strip()
    photo_path = photo_path_var.get()

    if not all([first_name, last_name, course, section, photo_path]):
        messagebox.showerror("Error", "Please fill all fields and select a photo.")
        return

    full_name = f"{first_name} {last_name}"
    image_name = f"{last_name.upper()}_{first_name.upper()}"

    os.makedirs("student_images", exist_ok=True)
    ext = os.path.splitext(photo_path)[1]
    new_image_path = os.path.join("student_images", f"{image_name}{ext}")
    shutil.copy(photo_path, new_image_path)

    db_file = "students.csv"
    file_exists = os.path.isfile(db_file)
    with open(db_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Image_Name', 'Full_Name', 'Course', 'Section'])
        writer.writerow([image_name, full_name, course, section])

    messagebox.showinfo("Success", f"Added {full_name} to database!")
    entry_first.delete(0, tk.END)
    entry_last.delete(0, tk.END)
    entry_course.delete(0, tk.END)
    entry_section.delete(0, tk.END)
    photo_path_var.set("")

# --- 2. CLASS SESSION SETTINGS ---
def save_session():
    config = {
        "subject": entry_subject.get().strip(),
        "professor": entry_prof.get().strip(),
        "day": entry_day.get().strip(),
        "start_time": entry_start.get().strip(),
        "late_mins": entry_late.get().strip()
    }
    # Saves the rules to a file that the camera can read later
    with open("session_config.json", "w") as f:
        json.dump(config, f)
    messagebox.showinfo("Session Saved", "Class rules updated! The camera will now use these settings.")

# --- 3. DATABASE VIEWERS ---
def view_database():
    view_window = tk.Toplevel(root)
    view_window.title("Master Student Database")
    view_window.geometry("600x400")
    columns = ("Image_ID", "Full_Name", "Course", "Section")
    tree = ttk.Treeview(view_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=140)
    scrollbar = ttk.Scrollbar(view_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(fill=tk.BOTH, expand=True)

    if os.path.isfile("students.csv"):
        with open("students.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tree.insert("", tk.END, values=(row["Image_Name"], row["Full_Name"], row["Course"], row["Section"]))

def view_attendance():
    today_date = datetime.now().strftime('%b_%d_%Y')
    db_file = f"Attendance_{today_date}.csv"
    students_file = "students.csv"

    view_window = tk.Toplevel(root)
    view_window.title(f"Live Attendance Report: {today_date}")
    view_window.geometry("800x400")

    columns = ("Full Name", "Course", "Section", "Time Logged", "Status")
    tree = ttk.Treeview(view_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    scrollbar = ttk.Scrollbar(view_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(fill=tk.BOTH, expand=True)

    all_students = {}
    if os.path.isfile(students_file):
        with open(students_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_students[row["Full_Name"]] = {"Course": row["Course"], "Section": row["Section"]}

    present_students = {}
    if os.path.isfile(db_file):
        with open(db_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                present_students[row["Full Name"]] = {"Time": row["Time"], "Status": row["Status"]}

    # The Logic Engine: Compares who is registered vs who actually showed up
    for name, details in all_students.items():
        if name in present_students:
            time_log = present_students[name]["Time"]
            status = present_students[name]["Status"]
        else:
            time_log = "--:--:--"
            status = "ABSENT" # Automatically marks missing students!
            
        tree.insert("", tk.END, values=(name, details["Course"], details["Section"], time_log, status))

# --- GUI WINDOW LAYOUT ---
root = tk.Tk()
root.title("University Command Center")
root.geometry("850x550")

top_frame = tk.Frame(root)
top_frame.pack(fill=tk.BOTH, expand=True)

# LEFT PANEL: Add Student
frame_left = tk.LabelFrame(top_frame, text="1. Register New Student", padx=15, pady=15, font=("Arial", 12, "bold"))
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Label(frame_left, text="First Name:").pack(anchor="w")
entry_first = tk.Entry(frame_left, width=30)
entry_first.pack(pady=2)

tk.Label(frame_left, text="Last Name:").pack(anchor="w")
entry_last = tk.Entry(frame_left, width=30)
entry_last.pack(pady=2)

tk.Label(frame_left, text="Course:").pack(anchor="w")
entry_course = tk.Entry(frame_left, width=30)
entry_course.pack(pady=2)

tk.Label(frame_left, text="Section:").pack(anchor="w")
entry_section = tk.Entry(frame_left, width=30)
entry_section.pack(pady=2)

photo_path_var = tk.StringVar()
tk.Button(frame_left, text="Select Photo", command=upload_photo).pack(pady=10)
tk.Label(frame_left, textvariable=photo_path_var, fg="gray", font=("Arial", 8)).pack()
tk.Button(frame_left, text="Save Student", font=("Arial", 11, "bold"), command=save_student).pack(pady=10)

# RIGHT PANEL: Session Setup
frame_right = tk.LabelFrame(top_frame, text="2. Class Session Settings", padx=15, pady=15, font=("Arial", 12, "bold"))
frame_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Label(frame_right, text="Subject Name:").pack(anchor="w")
entry_subject = tk.Entry(frame_right, width=30)
entry_subject.insert(0, "Intelligent Systems")
entry_subject.pack(pady=2)

tk.Label(frame_right, text="Professor:").pack(anchor="w")
entry_prof = tk.Entry(frame_right, width=30)
entry_prof.insert(0, "Prof. Dela Cruz")
entry_prof.pack(pady=2)

tk.Label(frame_right, text="Day of Week:").pack(anchor="w")
entry_day = tk.Entry(frame_right, width=30)
entry_day.insert(0, "Monday")
entry_day.pack(pady=2)

tk.Label(frame_right, text="Start Time (HH:MM):").pack(anchor="w")
entry_start = tk.Entry(frame_right, width=30)
entry_start.insert(0, "09:00")
entry_start.pack(pady=2)

tk.Label(frame_right, text="Late After (Minutes):").pack(anchor="w")
entry_late = tk.Entry(frame_right, width=30)
entry_late.insert(0, "15")
entry_late.pack(pady=2)

tk.Button(frame_right, text="Save Class Rules", font=("Arial", 11, "bold"), command=save_session).pack(pady=20)

# BOTTOM PANEL: Viewers
frame_bottom = tk.LabelFrame(root, text="3. Database Viewers", padx=15, pady=10, font=("Arial", 12, "bold"))
frame_bottom.pack(fill=tk.X, padx=10, pady=10)

tk.Button(frame_bottom, text="📄 View Master Student List", font=("Arial", 11), command=view_database).pack(side=tk.LEFT, padx=20, expand=True)
tk.Button(frame_bottom, text="📊 View Today's Attendance Log", font=("Arial", 11, "bold"), command=view_attendance).pack(side=tk.RIGHT, padx=20, expand=True)

root.mainloop()