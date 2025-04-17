import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from PIL import ImageTk, Image


# Train Image
def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message,text_to_speech):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcasecade_path)
    faces, Id = getImagesAndLables(trainimage_path)
    recognizer.train(faces, np.array(Id))
    recognizer.save(trainimagelabel_path)
    res = "Image Trained successfully"  # +",".join(str(f) for f in Id)
    message.configure(text=res)
    text_to_speech(res)


# def getImagesAndLables(path):
#     # imagePath = [os.path.join(path, f) for d in os.listdir(path) for f in d]
#     newdir = [os.path.join(path, d) for d in os.listdir(path)]
#     imagePath = [
#         os.path.join(newdir[i], f)
#         for i in range(len(newdir))
#         for f in os.listdir(newdir[i])
#     ]
#     faces = []
#     Ids = []
#     for imagePath in imagePath:
#         pilImage = Image.open(imagePath).convert("L")
#         imageNp = np.array(pilImage, "uint8")
#         Id = int(os.path.split(imagePath)[-1].split("_")[1])
#         faces.append(imageNp)
#         Ids.append(Id)
#     return faces, Ids

def getImagesAndLables(path):
    imagePaths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(root, file)
                imagePaths.append(full_path)

    print(f"[DEBUG] Found {len(imagePaths)} image files in: {path}")
    
    faces = []
    Ids = []

    for imagePath in imagePaths:
        try:
            pilImage = Image.open(imagePath).convert("L")  # Convert to grayscale
            imageNp = np.array(pilImage, "uint8")

            filename = os.path.basename(imagePath)
            # Example filename: 1_1 1_1_1.jpg
            # We assume ID is the first number before any underscore or space
            Id_str = filename.split("_")[0].split(" ")[0]
            Id = int(Id_str)

            faces.append(imageNp)
            Ids.append(Id)
            print(f"[DEBUG] Processed image {filename}, ID: {Id}")
        except Exception as e:
            print(f"[WARN] Skipping {imagePath}: {e}")

    print(f"[DEBUG] Total faces: {len(faces)}")
    return faces, Ids
