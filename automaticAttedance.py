import tkinter as tk
from tkinter import *
import os
import cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font
import subprocess
import platform

# Paths (cross-platform)
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = os.path.join("TrainingImageLabel", "Trainner.yml")
trainimage_path = "TrainingImage"
studentdetail_path = os.path.join("StudentDetails", "studentdetails.csv")
attendance_path = "Attendance"

# Platform-independent folder opener
def open_folder(path):
    system_platform = platform.system()
    if system_platform == "Darwin":  # macOS
        subprocess.Popen(["open", path])
    elif system_platform == "Windows":
        os.startfile(path)
    elif system_platform == "Linux":
        subprocess.Popen(["xdg-open", path])
    else:
        print(f"Unsupported OS: {system_platform}")

# Main Function
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20
        if sub == "":
            text_to_speech("Please enter the subject name!!!")
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found, please train model"
                    Notifica.configure(
                        text=e,
                        bg="black",
                        fg="yellow",
                        width=33,
                        font=("times", 15, "bold"),
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)
                    return

                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)

                while True:
                    _, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id, Subject, aa, date, timeStamp
                        Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                        if conf < 70:
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            tt = str(Id) + "-" + str(aa[0])
                            attendance.loc[len(attendance)] = [Id, aa[0]]
                            cv2.rectangle(im, (x, y), (x+w, y+h), (0, 260, 0), 4)
                            cv2.putText(im, str(tt), (x+h, y), font, 1, (255, 255, 0,), 4)
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x+w, y+h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x+h, y), font, 1, (0, 25, 255), 4)

                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                path = os.path.join(attendance_path, Subject)
                if not os.path.exists(path):
                    os.makedirs(path)
                fileName = os.path.join(
                    path, f"{Subject}_{date}_{Hour}-{Minute}-{Second}.csv"
                )
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                attendance.to_csv(fileName, index=False)

                m = f"Attendance Filled Successfully of {Subject}"
                Notifica.configure(
                    text=m,
                    bg="black",
                    fg="yellow",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("times", 15, "bold"),
                )
                text_to_speech(m)
                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                root = tk.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background="black")

                with open(fileName, newline="") as file:
                    reader = csv.reader(file)
                    for r, col in enumerate(reader):
                        for c, row in enumerate(col):
                            label = tk.Label(
                                root,
                                width=10,
                                height=1,
                                fg="yellow",
                                font=("times", 15, " bold "),
                                bg="black",
                                text=row,
                                relief=RIDGE,
                            )
                            label.grid(row=r, column=c)
                root.mainloop()

            except Exception as e:
                print("Error:", e)
                text_to_speech("No Face found for attendance")
                cv2.destroyAllWindows()

    def Attf():
        sub = tx.get()
        if sub == "":
            text_to_speech("Please enter the subject name!!!")
        else:
            path = os.path.join(attendance_path, sub)
            open_folder(path)

    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)

    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="black",
        fg="#00796b",  # Darker green text for contrast
        font=("arial", 25),
    )
    titl.place(x=160, y=12)

    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="black",
        fg="green",  # Yellow text for notification
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="#005f6a",  # Dark blue background
        fg="white",  # White text color
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",  # Yellow text color
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",  # Yellow text color
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="#005f6a",  # Dark blue background
        fg="white",  # White text color
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)

    subject.mainloop()
