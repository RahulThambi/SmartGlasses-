# import face_recognition
# import cv2
# import os
# import numpy as np

# def load_known_faces(folder_path):
#     known_face_encodings = []
#     known_face_names = []

#     for filename in os.listdir(folder_path):
#         if filename.endswith((".jpg", ".png", ".jpeg")):
#             image_path = os.path.join(folder_path, filename)
#             image = face_recognition.load_image_file(image_path)
#             face_encodings = face_recognition.face_encodings(image)

#             if face_encodings:
#                 known_face_encodings.append(face_encodings[0])
#                 name = os.path.splitext(filename)[0]
#                 known_face_names.append(name)
#             else:
#                 print(f"No faces found in image: {image_path}")

#     return known_face_encodings, known_face_names

# def main():
#     folder_path = r"G:\My Drive\Documents\BTECH SEVENTH SEM\CAPSTONE\FACE DETECTION\data"

#     if not os.path.exists(folder_path):
#         print(f"Error: The specified folder path does not exist: {folder_path}")
#         return

#     known_face_encodings, known_face_names = load_known_faces(folder_path)

#     if len(known_face_encodings) == 0:
#         print("No known faces found in the specified folder. Please add some images and try again.")
#         return

#     video_capture = cv2.VideoCapture(0)

#     while True:
#         ret, frame = video_capture.read()
#         if not ret:
#             print("Failed to capture frame")
#             break

#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         face_locations = face_recognition.face_locations(rgb_frame)
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#         for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#             name = "Unknown"

#             face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#             best_match_index = np.argmin(face_distances)

#             if matches[best_match_index]:
#                 name = known_face_names[best_match_index]

#             cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#             cv2.putText(frame, name, (left + 6, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 1)

#         cv2.imshow('Video', frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     video_capture.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

import face_recognition
import cv2
import os
import numpy as np
import pyttsx3
import time
from collections import Counter

def load_known_faces(folder_path):
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(folder_path):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            image_path = os.path.join(folder_path, filename)
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)

            if face_encodings:
                known_face_encodings.append(face_encodings[0])
                name = os.path.splitext(filename)[0]
                known_face_names.append(name)
            else:
                print(f"No faces found in image: {image_path}")

    return known_face_encodings, known_face_names

def announce_name_and_description(name, folder_path):
    description_file = os.path.join(folder_path, f"{name}.txt")
    if os.path.exists(description_file):
        with open(description_file, 'r') as file:
            description = file.read()
    else:
        description = "No description available."

    engine = pyttsx3.init()
    engine.say(f"This is {name}. {description}")
    engine.runAndWait()

def save_new_face(frame, face_encoding, name, description, folder_path, known_face_encodings, known_face_names):
    image_path = os.path.join(folder_path, f"{name}.jpg")
    cv2.imwrite(image_path, frame)
    
    description_file = os.path.join(folder_path, f"{name}.txt")
    with open(description_file, 'w') as file:
        file.write(description)
    
    known_face_encodings.append(face_encoding)
    known_face_names.append(name)

def main():
    folder_path = r"G:\My Drive\Documents\BTECH SEVENTH SEM\CAPSTONE\jarvis\data"

    if not os.path.exists(folder_path):
        print(f"Error: The specified folder path does not exist: {folder_path}")
        return

    known_face_encodings, known_face_names = load_known_faces(folder_path)

    if len(known_face_encodings) == 0:
        print("No known faces found in the specified folder. Please add some images and try again.")
        return

    video_capture = cv2.VideoCapture(0)
    start_time = time.time()
    match_results = []
    frame_to_save = None

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture frame")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            match_results.append(name)

            if name == "Unknown":
                frame_to_save = frame

        # Check if 2 seconds have passed
        if time.time() - start_time > 2:
            most_common_name = Counter(match_results).most_common(1)[0][0]
            
            if most_common_name != "Unknown":
                announce_name_and_description(most_common_name, folder_path)
            else:
                print("Unknown person detected.")
                engine = pyttsx3.init()
                engine.say("Unknown person detected. Please enter their name and description.")
                engine.runAndWait()

                # Ask for the new person's name and description
                new_name = input("Enter the name of the person: ")
                new_description = input("Enter the description of the person: ")

                if frame_to_save is not None:
                    save_new_face(frame_to_save, face_encodings[0], new_name, new_description, folder_path, known_face_encodings, known_face_names)

                engine.say(f"New person {new_name} has been saved.")
                engine.runAndWait()

            video_capture.release()
            cv2.destroyAllWindows()
            return

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
