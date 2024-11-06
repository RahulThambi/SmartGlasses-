import cv2
import time
import sys
import datetime
import os

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created folder: {folder_name}")

def countdown(duration):
    for i in range(duration, 0, -1):
        print(i)
        time.sleep(1)

def take_photo():
    create_folder("photos")
    cap = cv2.VideoCapture(0)
    countdown(3)
    ret, frame = cap.read()
    if ret:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join("photos", f"photo_{timestamp}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Photo saved as {filename}")
    cap.release()

def record_video():
    create_folder("videos")
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join("videos", f"video_{timestamp}.avi")
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
    
    countdown(3)
    print("Recording...")
    
    start_time = time.time()
    while time.time() - start_time < 10:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break
    
    cap.release()
    out.release()
    print(f"Video saved as {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python photo_video_capture.py [photo|video]")
        sys.exit(1)
    
    mode = sys.argv[1]
    if mode == "photo":
        take_photo()
    elif mode == "video":
        record_video()
    else:
        print("Invalid mode. Use 'photo' or 'video'.")