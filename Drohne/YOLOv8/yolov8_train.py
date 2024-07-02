from roboflow import Roboflow
from ultralytics import YOLO
import os

# Arbeitsverzeichnis wird auf das Daten Verzeichnis gesetzt
print("current working directory: ", os.getcwd())
os.chdir("/unix/bigdata/belehmann/PRJ_Flight_of_AI/YOLOv8/Tests_AuVAReS/")
print("current working directory: ", os.getcwd())

# Für das Laden der Daten aus Roboflow sollte model.train (line29) auskommentiert werden.
# Für das Training der KI sollte der Sektor für das Laden der Daten aus Roboflow auskommentiert werden. 

#Laden der Daten aus Roboflow; nach dem Laden die Pfade in der data.yaml Datei anpassen: 
# train: ../train/images
# val: ../val/images
#rf = Roboflow(api_key="ee7C5zP8x48FkWoho8kQ")
#project = rf.workspace("auvares-redball").project("auvares-red-ball-detection")
#version = project.version(11)
#dataset = version.download("yolov8")


#Laden eines neues Models
model = YOLO("yolov8n.pt")

# Trainieren des Models;
# data= "Pfad der data.yaml datei"
# epoch: Anzahl an Durchläufen/Trainingszyklen
# device: 0 = GPU
# batch: Anzahl Bilder im selbstgenerierten Bild (siehe runs/detect/trainX/train_batchX.jpg; Anpassbar je nach verfügbarem Grafikspeicher
#        Bei ConnectionRefusedError den Batchwert runtersetzen
# patience: default = 100; Wenn nach X Epochen keine Verbesserung, dann automatisch beenden
model.train(data="AuVAReS-red-ball-detection-11/data.yaml", epochs=2000, device=0,batch=300,patience=0)  

