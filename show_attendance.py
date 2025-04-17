
import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *
import subprocess

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return
        
        # Create file path in a cross-platform manner
        attendance_folder = os.path.join("Attendance", Subject)
        filenames = glob(os.path.join(attendance_folder, f"{Subject}*.csv"))
        
        # Check if no files are found
        if not filenames:
            t = f'No attendance files found for subject {Subject}.'
            text_to_speech(t)
            return
        
        # Read CSV files into DataFrames
        try:
            df = [pd.read_csv(f) for f in filenames]
        except Exception as e:
            t = f'Error reading files: {str(e)}'
            text_to_speech(t)
            return
        
        if len(df) == 0:
            t = 'No data found in the attendance files.'
            text_to_speech(t)
            return
        
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf["Attendance"].iloc[i] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'
        
        newdf.to_csv(os.path.join(attendance_folder, "attendance.csv"), index=False)

        root = tkinter.Tk()
        root.title("Attendance of " + Subject)
        root.configure(background="black")
        cs = os.path.join(attendance_folder, "attendance.csv")
        
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    label = tkinter.Label(
                        root,
                        width=10,
                        height=1,
                        fg="yellow",
                        font=("times", 15, " bold "),
                        bg="black",
                        text=row,
                        relief=tkinter.RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        root.mainloop()
        print(newdf)

    subject = Tk()
    subject.title("Subject Attendance")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)

    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            # Cross-platform file opening
            if os.name == 'nt':  # For Windows
                os.startfile(os.path.join("Attendance", sub))
            elif os.name == 'posix':  # For macOS/Linux
                subprocess.run(['open', os.path.join("Attendance", sub)])  # macOS
                # or subprocess.run(['xdg-open', os.path.join("Attendance", sub)])  # Linux

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
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
        fg="yellow",
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
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()
