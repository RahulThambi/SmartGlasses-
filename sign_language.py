# import cv2
# import numpy as np
# import os
# import time
# import pyttsx3
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.preprocessing import LabelEncoder
# import mediapipe as mp

# # Initialize MediaPipe
# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils
# hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# # Initialize text-to-speech engine
# engine = pyttsx3.init()

# # Paths
# signs_folder = r'G:\My Drive\Documents\BTECH SEVENTH SEM\CAPSTONE\jarvis\hand_signs'

# # Load features and labels from the folder
# def load_signs():
#     features = []
#     labels = []

#     for label in os.listdir(signs_folder):
#         label_folder = os.path.join(signs_folder, label)
#         if os.path.isdir(label_folder):
#             for filename in os.listdir(label_folder):
#                 if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
#                     img_path = os.path.join(label_folder, filename)
#                     img = cv2.imread(img_path)
#                     if img is not None:
#                         hand_landmarks = extract_hand_landmarks(img)
#                         if hand_landmarks is not None:
#                             features.append(hand_landmarks)
#                             labels.append(label)

#     return np.array(features), np.array(labels)

# # Extract hand landmarks from an image
# def extract_hand_landmarks(image):
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = hands.process(image_rgb)
#     if results.multi_hand_landmarks:
#         landmarks = []
#         for hand_landmarks in results.multi_hand_landmarks:
#             for landmark in hand_landmarks.landmark:
#                 landmarks.append([landmark.x, landmark.y, landmark.z])
#         return np.array(landmarks).flatten()
#     return None

# # Train a KNN model
# def train_knn(features, labels):
#     le = LabelEncoder()
#     labels_encoded = le.fit_transform(labels)
#     knn = KNeighborsClassifier(n_neighbors=3)
#     knn.fit(features, labels_encoded)
#     return knn, le

# def main():
#     features, labels = load_signs()
#     if len(features) == 0:
#         print("No sign data available.")
#         return

#     knn, label_encoder = train_knn(features, labels)

#     cap = cv2.VideoCapture(0)
#     print("Camera opened. Recognizing sign in 2 seconds...")

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Failed to capture frame")
#             break

#         hand_landmarks = extract_hand_landmarks(frame)
#         if hand_landmarks is not None:
#             hand_landmarks = hand_landmarks.reshape(1, -1)
#             prediction = knn.predict(hand_landmarks)
#             sign = label_encoder.inverse_transform(prediction)[0]
#             print(f"Recognized sign: {sign}")
#             engine.say(f"Recognized sign: {sign}")
#         else:
#             print("Unknown sign detected.")
#             engine.say("Unknown sign detected.")
#             engine.runAndWait()

#             # Ask user to input the sign
#             user_sign = input("Please enter the name of the sign: ")
#             new_sign_folder = os.path.join(signs_folder, user_sign)
#             os.makedirs(new_sign_folder, exist_ok=True)

#             # Save the image of the new sign
#             timestamp = time.strftime("%Y%m%d_%H%M%S")
#             image_path = os.path.join(new_sign_folder, f'{timestamp}.png')
#             cv2.imwrite(image_path, frame)

#             # Reload and retrain the model
#             features, labels = load_signs()
#             knn, label_encoder = train_knn(features, labels)

#             print("New sign added.")
#             engine.say("New sign added.")

#         engine.runAndWait()

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pyttsx3
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Paths
dataset_dir = r'G:\My Drive\Documents\BTECH SEVENTH SEM\CAPSTONE\jarvis\hand_signs'
model_path = r'G:\My Drive\Documents\BTECH SEVENTH SEM\CAPSTONE\jarvis\sign_language_model.h5'

def load_and_preprocess_data(dataset_dir):
    images = []
    labels = []
    class_names = os.listdir(dataset_dir)
    
    # Create a label encoder
    label_encoder = LabelEncoder()
    label_encoder.fit(class_names)
    
    for class_name in class_names:
        class_folder = os.path.join(dataset_dir, class_name)
        if os.path.isdir(class_folder):
            for filename in os.listdir(class_folder):
                if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                    img_path = os.path.join(class_folder, filename)
                    img = load_img(img_path, target_size=(64, 64))
                    img_array = img_to_array(img)
                    images.append(img_array)
                    labels.append(class_name)
    
    images = np.array(images) / 255.0  # Normalize images
    labels = np.array(labels)
    labels = label_encoder.transform(labels)  # Convert labels to numerical format
    return images, labels, label_encoder.classes_

def build_model(num_classes):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def train_model(model, X_train, y_train, X_val, y_val):
    early_stopping = EarlyStopping(monitor='val_loss', patience=3)
    history = model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val), callbacks=[early_stopping])
    return history

def save_model(model, model_path):
    model.save(model_path)

def load_model(model_path):
    if os.path.exists(model_path):
        try:
            return tf.keras.models.load_model(model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    else:
        print("Model file does not exist.")
        return None

def classify_sign(model, img_path, class_names):
    img = load_img(img_path, target_size=(64, 64))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions = model.predict(img_array)
    class_index = np.argmax(predictions)
    return class_names[class_index]

def capture_and_classify_sign(model, class_names):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    print("Camera opened. Recognizing sign in 2 seconds...")
    time.sleep(2)

    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        cap.release()
        cv2.destroyAllWindows()
        return

    # Save the captured image
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    image_path = f'captured_sign_{timestamp}.png'
    cv2.imwrite(image_path, frame)

    # Classify the captured sign
    recognized_sign = classify_sign(model, image_path, class_names)
    if recognized_sign:
        print(f"Recognized sign: {recognized_sign}")
        engine.say(f"Recognized sign: {recognized_sign}")
    else:
        print("Unknown sign detected.")
        engine.say("Unknown sign detected.")
        engine.runAndWait()
        
        # Ask user for new sign
        user_sign = input("Please enter the name of the new sign: ")
        new_sign_folder = os.path.join(dataset_dir, user_sign)
        os.makedirs(new_sign_folder, exist_ok=True)
        
        # Save the new sign image
        new_sign_path = os.path.join(new_sign_folder, f'{timestamp}.png')
        cv2.imwrite(new_sign_path, frame)
        
        # Reload and retrain the model
        X, y, class_names = load_and_preprocess_data(dataset_dir)
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        model = build_model(num_classes=len(class_names))
        train_model(model, X_train, y_train, X_val, y_val)
        save_model(model, model_path)

        print("New sign added and model updated.")
        engine.say("New sign added and model updated.")

    engine.runAndWait()
    cap.release()
    cv2.destroyAllWindows()

def main():
    model = load_model(model_path)
    if model is None:
        # Model does not exist or failed to load, need to train a new one
        print("Training new model...")
        X, y, class_names = load_and_preprocess_data(dataset_dir)
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        model = build_model(num_classes=len(class_names))
        train_model(model, X_train, y_train, X_val, y_val)
        save_model(model, model_path)

    capture_and_classify_sign(model, class_names)

if __name__ == "__main__":
    main()

