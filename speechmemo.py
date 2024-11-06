import speech_recognition as sr
import os
import time

# Initialize the recognizer
r = sr.Recognizer()

# Function to listen and recognize speech
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        return ""

# Create a directory to save the text file if it doesn't exist
if not os.path.exists("recorded_texts"):
    os.makedirs("recorded_texts")

# Function to save text to a file with a timestamp
def save_to_file(text):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"recorded_texts/recorded_text_{timestamp}.txt"
    with open(filename, "a") as f:
        f.write(text + "\n")
    return filename

print("Start speaking. Say 'okay stop' to stop recording.")

# Main loop to listen and save the text
while True:
    text = listen()
    
    if "okay stop" in text:
        print("Stopping the recording.")
        if text != "okay stop":
            filename = save_to_file(text.replace("okay stop", ""))
            print(f"Text saved to {filename}.")
        break
    
    if text:
        filename = save_to_file(text)
        print(f"Text saved to {filename}.")
        break

# Exit the script
print("Script has stopped.")