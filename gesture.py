
import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import speech_recognition as sr
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from math import hypot

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Initialize OpenCV
cap = cv2.VideoCapture(0)

# Initialize audio volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]

def listen_for_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Command recognized: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError:
        print("Could not request results")
        return ""

def control_volume(img, lmList):
    if lmList:
        x1, y1 = lmList[4][1], lmList[4][2]  # Thumb
        x2, y2 = lmList[8][1], lmList[8][2]  # Index finger
        length = hypot(x2 - x1, y2 - y1)
        vol = np.interp(length, [30, 350], [volMin, volMax])
        volbar = np.interp(length, [30, 350], [400, 150])
        volper = np.interp(length, [30, 350], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
        # Print volume level for debugging
        print(f"Volume level: {volper:.0f}%")

def control_zoom(landmarks):
    count = 0
    if landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y:
        count += 1
    if landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y:
        count += 1
    if count == 1:
        print("Zooming in")
        pyautogui.hotkey('ctrl', '+')  # Zoom in
    elif count == 2:
        print("Zooming out")
        pyautogui.hotkey('ctrl', '-')  # Zoom out

def process_mode(mode):
    start_time = time.time()
    while True:
        success, img = cap.read()
        if not success:
            print("Error: Failed to capture image")
            break
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        lmList = []
        if results.multi_hand_landmarks:
            for handlandmark in results.multi_hand_landmarks:
                for id, lm in enumerate(handlandmark.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_drawing.draw_landmarks(img, handlandmark, mp_hands.HAND_CONNECTIONS)
        
        if mode == 'volume':
            control_volume(img, lmList)
        elif mode == 'zoom':
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmarks = hand_landmarks.landmark
                    control_zoom(landmarks)
        
        # Check if time elapsed exceeds 10 seconds
        if time.time() - start_time > 10:
            print(f"{mode.capitalize()} mode deactivated after 10 seconds")
            break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

while True:
    command = listen_for_command()
    
    if "turn off" in command:
        print("Turning off. Exiting program.")
        break

    elif "volume" in command:
        print("Volume control mode activated.")
        process_mode('volume')
    
    elif "zoom" in command:
        print("Zoom control mode activated.")
        process_mode('zoom')
    
    elif "quit" in command:
        print("Exiting program.")
        break

    time.sleep(0.1)  # Short delay to prevent high CPU usage

cap.release()
cv2.destroyAllWindows()
