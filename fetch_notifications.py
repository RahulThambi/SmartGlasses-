
# import requests
# import time

# # Replace 'YOUR_ACCESS_TOKEN' with your Pushbullet API Key
# ACCESS_TOKEN = 'o.0MKEmwVJdvrzgwIdc4JkEeF7rMiKuaeC'
# URL_PUSHES = 'https://api.pushbullet.com/v2/pushes'

# def get_notifications():
#     headers = {
#         'Access-Token': ACCESS_TOKEN,
#         'Content-Type': 'application/json'
#     }
#     response = requests.get(URL_PUSHES, headers=headers)
#     if response.status_code == 200:
#         return response.json()['pushes']
#     else:
#         print("Failed to retrieve notifications")
#         return []

# def send_notification(title, message):
#     headers = {
#         'Access-Token': ACCESS_TOKEN,
#         'Content-Type': 'application/json'
#     }
#     data = {
#         'type': 'note',
#         'title': title,
#         'body': message
#     }
    
#     response = requests.post(URL_PUSHES, headers=headers, json=data)
    
#     if response.status_code == 200:
#         print("Notification sent successfully.")
#     else:
#         print("Failed to send notification:", response.text)

# if __name__ == "__main__":
#     seen_notifications = set()  # To track already seen notifications
    
#     while True:
#         # Get notifications
#         notifications = get_notifications()
        
#         for notification in notifications:
#             # Check if notification has already been seen
#             if notification['iden'] not in seen_notifications:
#                 sender = notification.get('sender_email', 'Unknown Sender')
#                 title = notification.get('title', 'No Title')
#                 body = notification.get('body', 'No Body')
                
#                 print(f"Notification from {sender}: {title} - {body}")
#                 seen_notifications.add(notification['iden'])

#         # Check for user input
#         user_input = input("Type 'send' to send a notification or 'recieve' to view notificatin or 'exit' to quit: ")
#         if user_input.lower() == 'exit':
#             break
#         elif user_input.lower() == 'send':
#             title = input("Enter notification title: ")
#             message = input("Enter your message: ")
#             send_notification(title, message)

#         # Wait before checking again (you can adjust this)
#         time.sleep(5)  # Reduced sleep time for more frequent checks

# fetch_notifications.py
# above code is manual keyboard cli

#below code is voice automated but wihtout gui
# import requests
# import time
# import speech_recognition as sr
# import pyttsx3

# class VoiceNotificationSystem:
#     def __init__(self):
#         self.ACCESS_TOKEN = 'o.0MKEmwVJdvrzgwIdc4JkEeF7rMiKuaeC'
#         self.URL_PUSHES = 'https://api.pushbullet.com/v2/pushes'
#         self.recognizer = sr.Recognizer()
#         self.engine = pyttsx3.init()
#         self.seen_notifications = set()

#     def speak(self, text):
#         print(f"Assistant: {text}")
#         self.engine.say(text)
#         self.engine.runAndWait()

#     def listen(self):
#         with sr.Microphone() as source:
#             print("Listening...")
#             audio = self.recognizer.listen(source)
#         try:
#             text = self.recognizer.recognize_google(audio)
#             print(f"You said: {text}")
#             return text.lower()
#         except sr.UnknownValueError:
#             print("Could not understand audio")
#             return ""
#         except sr.RequestError as e:
#             print(f"Could not request results; {e}")
#             return ""

#     def get_notifications(self):
#         headers = {
#             'Access-Token': self.ACCESS_TOKEN,
#             'Content-Type': 'application/json'
#         }
#         response = requests.get(self.URL_PUSHES, headers=headers)
#         if response.status_code == 200:
#             return response.json()['pushes']
#         else:
#             self.speak("Failed to retrieve notifications")
#             return []

#     def send_notification(self, title, message):
#         headers = {
#             'Access-Token': self.ACCESS_TOKEN,
#             'Content-Type': 'application/json'
#         }
#         data = {
#             'type': 'note',
#             'title': title,
#             'body': message
#         }
        
#         response = requests.post(self.URL_PUSHES, headers=headers, json=data)
        
#         if response.status_code == 200:
#             self.speak("Notification sent successfully.")
#             return True
#         else:
#             self.speak("Failed to send notification.")
#             return False

#     def check_new_notifications(self):
#         notifications = self.get_notifications()
#         new_notifications = []
        
#         for notification in notifications:
#             if notification['iden'] not in self.seen_notifications:
#                 sender = notification.get('sender_email', 'Unknown Sender')
#                 title = notification.get('title', 'No Title')
#                 body = notification.get('body', 'No Body')
#                 new_notifications.append((sender, title, body))
#                 self.seen_notifications.add(notification['iden'])
        
#         return new_notifications

#     def handle_voice_notifications(self):
#         self.speak("Notification system activated. Would you like to send a notification or check received notifications?")
        
#         while True:
#             command = self.listen()
            
#             if 'send' in command:
#                 self.speak("What should be the title of your notification?")
#                 title = self.listen()
                
#                 self.speak("What message would you like to send?")
#                 message = self.listen()
                
#                 self.speak(f"I'll send a notification with title: {title} and message: {message}. Say 'confirm' to send or 'cancel' to abort.")
                
#                 confirmation = self.listen()
#                 if 'confirm' in confirmation:
#                     self.send_notification(title, message)
#                 elif 'cancel' in confirmation:
#                     self.speak("Sending cancelled.")
                
#             elif 'check' in command or 'receive' in command:
#                 new_notifications = self.check_new_notifications()
#                 if new_notifications:
#                     self.speak("Here are your new notifications:")
#                     for sender, title, body in new_notifications:
#                         self.speak(f"From {sender}: {title} - {body}")
#                 else:
#                     self.speak("No new notifications.")
            
#             elif 'exit' in command or 'quit' in command:
#                 self.speak("Exiting notification system.")
#                 break
            
#             self.speak("Would you like to do anything else with notifications?")

# def main():
#     notification_system = VoiceNotificationSystem()
#     notification_system.handle_voice_notifications()

# if __name__ == "__main__":
#     main()


# fetch_notifications.py

import requests
import time
import speech_recognition as sr
import pyttsx3
from datetime import datetime

class VoiceNotificationSystem:
    def __init__(self, gui_queue):
        self.ACCESS_TOKEN = 'o.0MKEmwVJdvrzgwIdc4JkEeF7rMiKuaeC'
        self.URL_PUSHES = 'https://api.pushbullet.com/v2/pushes'
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.seen_notifications = set()
        self.gui_queue = gui_queue

    def send_to_gui(self, content, source="system"):
        self.gui_queue.put({
            'type': 'message',
            'source': source,
            'content': content,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })

    def update_status(self, status):
        self.gui_queue.put({
            'type': 'status',
            'value': status
        })

    def speak(self, text):
        self.send_to_gui(text, "jarvis")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.update_status("LISTENING")
            self.send_to_gui("Listening...", "system")
            audio = self.recognizer.listen(source)
        try:
            text = self.recognizer.recognize_google(audio)
            self.send_to_gui(f"You said: {text}", "user")
            return text.lower()
        except sr.UnknownValueError:
            self.send_to_gui("Could not understand audio", "system")
            return ""
        except sr.RequestError as e:
            self.send_to_gui(f"Could not request results; {e}", "system")
            return ""

    def get_notifications(self):
        self.update_status("PROCESSING")
        headers = {
            'Access-Token': self.ACCESS_TOKEN,
            'Content-Type': 'application/json'
        }
        response = requests.get(self.URL_PUSHES, headers=headers)
        self.update_status("STANDBY")
        
        if response.status_code == 200:
            return response.json()['pushes']
        else:
            self.speak("Failed to retrieve notifications")
            self.send_to_gui("Failed to retrieve notifications", "system")
            return []

    def send_notification(self, title, message):
        self.update_status("PROCESSING")
        headers = {
            'Access-Token': self.ACCESS_TOKEN,
            'Content-Type': 'application/json'
        }
        data = {
            'type': 'note',
            'title': title,
            'body': message
        }
        
        response = requests.post(self.URL_PUSHES, headers=headers, json=data)
        
        if response.status_code == 200:
            self.speak("Notification sent successfully.")
            self.send_to_gui(f"✅ Notification sent - Title: {title}, Message: {message}", "system")
            return True
        else:
            self.speak("Failed to send notification.")
            self.send_to_gui("❌ Failed to send notification", "system")
            return False

    def check_new_notifications(self):
        notifications = self.get_notifications()
        new_notifications = []
        
        for notification in notifications:
            if notification['iden'] not in self.seen_notifications:
                sender = notification.get('sender_email', 'Unknown Sender')
                title = notification.get('title', 'No Title')
                body = notification.get('body', 'No Body')
                new_notifications.append((sender, title, body))
                self.seen_notifications.add(notification['iden'])
                # Display each notification in GUI
                self.send_to_gui(f"📬 New notification from {sender}:\nTitle: {title}\nMessage: {body}", "system")
        
        return new_notifications

    def handle_voice_notifications(self):
        self.speak("Notification system activated. Would you like to send a notification or check received notifications?")
        self.update_status("LISTENING")
        
        while True:
            command = self.listen()
            
            if 'send' in command:
                self.speak("What should be the title of your notification?")
                title = self.listen()
                
                self.speak("What message would you like to send?")
                message = self.listen()
                
                self.speak(f"I'll send a notification with title: {title} and message: {message}. Say 'confirm' to send or 'cancel' to abort.")
                self.send_to_gui(f"📝 Preview:\nTitle: {title}\nMessage: {message}\n(Say 'confirm' to send or 'cancel' to abort)", "system")
                
                confirmation = self.listen()
                if 'confirm' in confirmation:
                    self.send_notification(title, message)
                elif 'cancel' in confirmation:
                    self.speak("Sending cancelled.")
                    self.send_to_gui("❌ Notification cancelled", "system")
                
            elif 'check' in command or 'receive' in command:
                self.speak("Checking for new notifications.")
                self.send_to_gui("🔍 Checking for new notifications...", "system")
                new_notifications = self.check_new_notifications()
                if new_notifications:
                    self.speak("Here are your new notifications:")
                    for sender, title, body in new_notifications:
                        notification_text = f"From {sender}: {title} - {body}"
                        self.speak(notification_text)
                else:
                    self.speak("No new notifications.")
                    self.send_to_gui("📭 No new notifications", "system")
            
            elif 'exit' in command or 'quit' in command:
                self.speak("Exiting notification system.")
                self.send_to_gui("👋 Notification system deactivated", "system")
                break
            
            self.speak("Would you like to do anything else with notifications?")
            self.update_status("LISTENING")

def main():
    # This is just for testing the script independently
    from queue import Queue
    gui_queue = Queue()
    notification_system = VoiceNotificationSystem(gui_queue)
    notification_system.handle_voice_notifications()

if __name__ == "__main__":
    main()