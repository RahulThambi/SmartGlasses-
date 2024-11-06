import cv2
import numpy as np
from gtts import gTTS
from playsound import playsound
import os
import time

def speech(text):
    print(text)
    language = "en"
    output = gTTS(text=text, lang=language, slow=False)
    output_path = r"G:\My Drive\Documents\BTECH SEVENTH SEM\CAPSTONE\OBJECT DETECTION\output.mp3"
    output.save(output_path)
    playsound(output_path)

def detect_objects(frame):
    # Paths to the YOLO model files
    model_cfg = r"G:\My Drive\Documents\BTECH SEVENTH SEM\CAPSTONE\OBJECT DETECTION\yolov3.cfg"
    model_weights = r"G:\My Drive\Documents\BTECH SEVENTH SEM\CAPSTONE\OBJECT DETECTION\yolov3.weights"
    model_labels = r"G:\My Drive\Documents\BTECH SEVENTH SEM\CAPSTONE\OBJECT DETECTION\coco.names"

    # Load YOLO model
    net = cv2.dnn.readNet(model_weights, model_cfg)

    # Load labels
    with open(model_labels, 'r') as f:
        classes = f.read().strip().split('\n')

    # Prepare the image for YOLO
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(net.getUnconnectedOutLayersNames())

    # Process the outputs
    class_ids = []
    confidences = []
    boxes = []
    labels = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])
                x = center_x - w // 2
                y = center_y - h // 2
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    if len(indexes) > 0:
        for i in indexes.flatten():
            label = str(classes[class_ids[i]])
            if label not in labels:
                labels.append(label)

    return labels

# Attempt to open the camera
video = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not video.isOpened():
    print("Error: Could not open video device")
    exit()

print("Video device opened successfully")

# Wait for 2 seconds
time.sleep(2)

# Capture an image
ret, frame = video.read()
if not ret:
    print("Error: Failed to read frame from video device")
    video.release()
    cv2.destroyAllWindows()
    exit()

# Detect objects
labels = detect_objects(frame)

# Release the video capture object
video.release()
cv2.destroyAllWindows()

# Narrate the detected objects
if labels:
    new_sentence = [f"I found a {label}" if i == 0 else f"a {label}," for i, label in enumerate(labels)]
    speech(" ".join(new_sentence))
else:
    speech("No objects detected.")

