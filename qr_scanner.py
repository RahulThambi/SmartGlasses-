# import cv2
# from pyzbar.pyzbar import decode
# import requests
# from bs4 import BeautifulSoup
# import pyttsx3

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# # Start capturing video from the camera
# cap = cv2.VideoCapture(0)

# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Decode QR codes in the frame
#     qr_codes = decode(frame)
#     for qr_code in qr_codes:
#         # Extract the data from the QR code
#         qr_data = qr_code.data.decode('utf-8')
#         print(f"QR Code detected: {qr_data}")

#         # Fetch the content of the URL
#         try:
#             response = requests.get(qr_data)
#             if response.status_code == 200:
#                 # Parse the HTML content
#                 soup = BeautifulSoup(response.text, 'html.parser')
#                 # Extract text from the HTML
#                 page_text = soup.get_text()
#                 # Speak out the page content
#                 speak(page_text)
#             else:
#                 speak("Failed to retrieve the content from the URL.")
#         except requests.RequestException as e:
#             speak(f"An error occurred: {e}")

#         # Display the QR code detection
#         cv2.rectangle(frame, (qr_code.rect.left, qr_code.rect.top),
#                       (qr_code.rect.left + qr_code.rect.width, qr_code.rect.top + qr_code.rect.height),
#                       (0, 255, 0), 2)

#     # Display the resulting frame
#     cv2.imshow('QR Code Scanner', frame)

#     # Break the loop when 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the camera and close all OpenCV windows
# cap.release()
# cv2.destroyAllWindows()






# import cv2
# from pyzbar.pyzbar import decode
# import pyttsx3

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# # Start capturing video from the camera
# cap = cv2.VideoCapture(0)

# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Decode QR codes in the frame
#     qr_codes = decode(frame)
#     for qr_code in qr_codes:
#         # Extract the data from the QR code
#         qr_data = qr_code.data.decode('utf-8')
#         print(f"QR Code detected: {qr_data}")

#         # Check if the data is a URL or plain text
#         if qr_data.startswith('http://') or qr_data.startswith('https://'):
#             # It's a URL
#             description = "This QR code contains a link to a website."
#         else:
#             # It's plain text
#             description = f"This QR code contains the following text: {qr_data}"

#         # Speak out the description
#         speak(description)

#         # Display the QR code detection
#         cv2.rectangle(frame, (qr_code.rect.left, qr_code.rect.top),
#                       (qr_code.rect.left + qr_code.rect.width, qr_code.rect.top + qr_code.rect.height),
#                       (0, 255, 0), 2)

#     # Display the resulting frame
#     cv2.imshow('QR Code Scanner', frame)

#     # Break the loop when 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the camera and close all OpenCV windows
# cap.release()
# cv2.destroyAllWindows()


import cv2
from pyzbar.pyzbar import decode
import requests
from bs4 import BeautifulSoup

def get_website_title(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the title of the webpage
            title = soup.title.string if soup.title else "No title found"
            return title
        else:
            return "Website unreachable"
    except requests.RequestException as e:
        return "Error accessing website"

def scan_qr_code():
    cap = cv2.VideoCapture(0)
    qr_code_detected = False

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # Decode QR codes in the frame
        qr_codes = decode(frame)
        for qr_code in qr_codes:
            # Extract the data from the QR code
            qr_data = qr_code.data.decode('utf-8')
            if qr_data.startswith('http://') or qr_data.startswith('https://'):
                # Get website title
                title = get_website_title(qr_data)
                cap.release()
                cv2.destroyAllWindows()
                return title

            # Display the QR code detection
            cv2.rectangle(frame, (qr_code.rect.left, qr_code.rect.top),
                          (qr_code.rect.left + qr_code.rect.width, qr_code.rect.top + qr_code.rect.height),
                          (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('QR Code Scanner', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
