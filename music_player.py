# import os
# import pygame
# import speech_recognition as sr
# from fuzzywuzzy import process
# import time
# import pyttsx3

# engine = pyttsx3.init()


# def search_song(directory, song_name):
#     files = []
#     for root, dirs, filenames in os.walk(directory):
#         for filename in filenames:
#             files.append(os.path.join(root, filename))
#     closest_match, _ = process.extractOne(song_name, files, scorer=process.fuzz.partial_ratio)
#     return closest_match

# def play_song(song_path):
#     if song_path:
#         pygame.mixer.music.load(song_path)
#         pygame.mixer.music.play()
#         print(f"Playing song: {song_path}")
#         speak("playing: {song_path}")
#         return True
#     else:
#         print("Song not found!")
#         speak("Song not found!")

#         return False

# def get_song_name_from_speech():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         speak("Listening for song name")
#         print("Listening for song name...")
#         audio = recognizer.listen(source)
#         try:
#             song_name = recognizer.recognize_google(audio)
#             print(f"Song name recognized: {song_name}")
#             return song_name
#         except sr.UnknownValueError:
#             print("Sorry, could not understand the audio.")
#             return None
#         except sr.RequestError:
#             print("Sorry, there was an error with the speech recognition service.")
#             return None
# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def listen_for_commands():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         while True:
#             print("Listening for commands...")
#             audio = recognizer.listen(source)
#             try:
#                 command = recognizer.recognize_google(audio).lower()
#                 print(f"Command recognized: {command}")

#                 if "hold" in command:
#                     pygame.mixer.music.pause()
#                     print("Music paused.")
#                     speak("Music paused")

#                 elif "resume" in command:
#                     pygame.mixer.music.unpause()
#                     print("Music resumed.")
#                     speak("Music resumed")

#                 elif "stop" in command:
#                     pygame.mixer.music.stop()
#                     print("Music stopped.")
#                     speak("Music stopped")

#                     break
#                 else:
#                     print("Command not recognized.")
#                 time.sleep(1)  # Adding a short delay

#             except sr.UnknownValueError:
#                 print("Sorry, could not understand the audio.")
#             except sr.RequestError:
#                 print("Sorry, there was an error with the speech recognition service.")

# if __name__ == "__main__":
#     pygame.mixer.init()  # Initialize pygame mixer here
#     song_directory = r"G:\My Drive\Documents\BTECH SEVENTH SEM\CAPSTONE\jarvis\songs"
#     song_name = get_song_name_from_speech()

#     if song_name:
#         song_path = search_song(song_directory, song_name)
#         if play_song(song_path):
#             listen_for_commands()
#     else:
#         print("No song name provided.")





# import os
# import pygame
# import speech_recognition as sr
# from fuzzywuzzy import process
# import time
# import pyttsx3
# import threading
# import keyboard  # You may need to install this library with 'pip install keyboard'

# engine = pyttsx3.init()

# def search_song(directory, song_name):
#     files = []
#     for root, dirs, filenames in os.walk(directory):
#         for filename in filenames:
#             files.append(os.path.join(root, filename))
#     closest_match, _ = process.extractOne(song_name, files, scorer=process.fuzz.partial_ratio)
#     return closest_match

# def play_song(song_path):
#     if song_path:
#         pygame.mixer.music.load(song_path)
#         pygame.mixer.music.play()
#         print(f"Playing song: {song_path}")
#         speak(f"Playing: {song_path}")
#         return True
#     else:
#         print("Song not found!")
#         speak("Song not found!")
#         return False

# def get_song_name_from_speech():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         speak("Listening for song name")
#         print("Listening for song name...")
#         audio = recognizer.listen(source)
#         try:
#             song_name = recognizer.recognize_google(audio)
#             print(f"Song name recognized: {song_name}")
#             return song_name
#         except sr.UnknownValueError:
#             print("Sorry, could not understand the audio.")
#             return None
#         except sr.RequestError:
#             print("Sorry, there was an error with the speech recognition service.")
#             return None

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def listen_for_commands():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         while True:
#             print("Listening for commands...")
#             audio = recognizer.listen(source)
#             try:
#                 command = recognizer.recognize_google(audio).lower()
#                 print(f"Command recognized: {command}")

#                 if "hold" in command:
#                     pygame.mixer.music.pause()
#                     print("Music paused.")
#                     speak("Music paused")

#                 elif "resume" in command:
#                     pygame.mixer.music.unpause()
#                     print("Music resumed.")
#                     speak("Music resumed")

#                 elif "stop" in command:
#                     pygame.mixer.music.stop()
#                     print("Music stopped.")
#                     speak("Music stopped")
#                     break
#                 else:
#                     print("Command not recognized.")
#                 time.sleep(1)  # Adding a short delay

#             except sr.UnknownValueError:
#                 print("Sorry, could not understand the audio.")
#             except sr.RequestError:
#                 print("Sorry, there was an error with the speech recognition service.")

# def exit_on_x():
#     print("Press 'X' to stop the program.")
#     while True:
#         if keyboard.is_pressed("q"):
#             print("Exit key 'q' pressed.")
#             pygame.mixer.music.stop()
#             speak("Exiting program.")
#             break

# if __name__ == "__main__":
#     pygame.mixer.init()  # Initialize pygame mixer here
#     song_directory = r"G:\My Drive\Documents\BTECH SEVENTH SEM\CAPSTONE\jarvis\songs"
#     song_name = get_song_name_from_speech()

#     if song_name:
#         song_path = search_song(song_directory, song_name)
#         if play_song(song_path):
#             # Start the exit listener thread
#             exit_thread = threading.Thread(target=exit_on_x, daemon=True)
#             exit_thread.start()
#             listen_for_commands()
#     else:
#         print("No song name provided.")



import os
import pygame
import speech_recognition as sr
from fuzzywuzzy import process
import time
import pyttsx3
import threading
import keyboard  # You may need to install this library with 'pip install keyboard'

engine = pyttsx3.init()
exit_flag = False  # Flag to exit to the root code

def search_song(directory, song_name):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    closest_match, _ = process.extractOne(song_name, files, scorer=process.fuzz.partial_ratio)
    return closest_match

def play_song(song_path):
    if song_path:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        print(f"Playing song: {song_path}")
        speak(f"Playing: {song_path}")
        return True
    else:
        print("Song not found!")
        speak("Song not found!")
        return False

def get_song_name_from_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for song name")
        print("Listening for song name...")
        audio = recognizer.listen(source)
        try:
            song_name = recognizer.recognize_google(audio)
            print(f"Song name recognized: {song_name}")
            return song_name
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
            return None
        except sr.RequestError:
            print("Sorry, there was an error with the speech recognition service.")
            return None

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_for_commands():
    global exit_flag
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Listening for commands...")
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio).lower()
                print(f"Command recognized: {command}")

                if "hold" in command:
                    pygame.mixer.music.pause()
                    print("Music paused.")
                    speak("Music paused")

                elif "resume" in command:
                    pygame.mixer.music.unpause()
                    print("Music resumed.")
                    speak("Music resumed")

                elif "stop" in command:
                    pygame.mixer.music.stop()
                    print("Music stopped.")
                    speak("Music stopped")
                    break

                elif "turn off" in command:
                    pygame.mixer.music.stop()
                    print("Turning off the program.")
                    speak("Turning off the program")
                    exit_flag = True
                    break

                else:
                    print("Command not recognized.")
                time.sleep(1)  # Adding a short delay

            except sr.UnknownValueError:
                print("Sorry, could not understand the audio.")
            except sr.RequestError:
                print("Sorry, there was an error with the speech recognition service.")
    return not exit_flag

def exit_on_x():
    global exit_flag
    print("Press 'Q' to stop the program.")
    while not exit_flag:
        if keyboard.is_pressed("q"):
            print("Exit key 'q' pressed.")
            pygame.mixer.music.stop()
            speak("Exiting to main menu.")
            exit_flag = True
            break

if __name__ == "__main__":
    pygame.mixer.init()  # Initialize pygame mixer here
    song_directory = r"G:\My Drive\Documents\BTECH SEVENTH SEM\CAPSTONE\jarvis\songs"

    while True:
        song_name = get_song_name_from_speech()
        
        if song_name:
            song_path = search_song(song_directory, song_name)
            if play_song(song_path):
                # Reset exit flag each time a new song plays
                exit_flag = False

                # Start the exit listener thread
                exit_thread = threading.Thread(target=exit_on_x, daemon=True)
                exit_thread.start()

                # Listen for commands and exit if "turn off" is heard
                if not listen_for_commands() or exit_flag:
                    print("Returning to root menu.")
                    exit_flag = False
                    continue
        else:
            print("No song name provided.")