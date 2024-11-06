import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import time
import datetime
import os

# Initialize OpenAI client (you'll need an API key)
client = OpenAI(api_key='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')

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize speech recognizer
r = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except:
        return ""

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant named Jarvis. Give all the response as accurate and concise as you can."},
            {"role": "user", "content": command}
        ]
    )
    return response.choices[0].message.content.strip()

def write_to_file(text, filename):
    with open(filename, 'a') as file:
        file.write(text + '\n')

def main():
    # Create 'conversations' folder if it doesn't exist
    if not os.path.exists('conversations'):
        os.makedirs('conversations')

    # Generate unique filename for this conversation
    filename = os.path.join('conversations', f"conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    speak("Conversation recording started. Say 'stop recording' to end.")
    
    while True:
        command = listen()
        if command:
            if "stop recording" in command:
                speak("Recording stopped. The conversation has been saved.")
                break
            
            response = process_command(command)
            speak(response)
            
            write_to_file(f"User: {command}", filename)
            write_to_file(f"Assistant: {response}", filename)
        
        time.sleep(0.1)  # Short delay to prevent high CPU usage

if __name__ == "__main__":
    main()