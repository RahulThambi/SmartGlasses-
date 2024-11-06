import json
import time
from datetime import datetime

# Define the path to the JSON file for storing reminders
FILE_PATH = r"G:\My Drive\Documents\BTECH SEVENTH SEM\CAPSTONE\jarvis\reminders.json"

# Load reminders from the JSON file
def load_reminders():
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save reminders to the JSON file
def save_reminders(reminders):
    with open(FILE_PATH, "w") as file:
        json.dump(reminders, file, indent=4)

# Add a new reminder
def add_reminder(reminder_text, reminder_time):
    reminders = load_reminders()
    reminder = {
        "text": reminder_text,
        "time": reminder_time,
        "completed": False
    }
    reminders.append(reminder)
    save_reminders(reminders)
    print("Reminder added successfully!")

# List all reminders with their status
def list_reminders():
    reminders = load_reminders()
    if not reminders:
        print("No reminders available.")
    else:
        for idx, reminder in enumerate(reminders, start=1):
            status = "Completed" if reminder["completed"] else "Pending"
            print(f"{idx}. {reminder['text']} - Due: {reminder['time']} [{status}]")

# Mark a reminder as complete
def mark_as_complete(index):
    reminders = load_reminders()
    if 0 <= index < len(reminders):
        reminders[index]["completed"] = True
        save_reminders(reminders)
        print("Reminder marked as complete!")
    else:
        print("Invalid reminder index.")

# Delete a reminder
def delete_reminder(index):
    reminders = load_reminders()
    if 0 <= index < len(reminders):
        del reminders[index]
        save_reminders(reminders)
        print("Reminder deleted successfully!")
    else:
        print("Invalid reminder index.")

# Count the total number of reminders
def count_reminders():
    reminders = load_reminders()
    print(f"You have {len(reminders)} reminders.")

# Check for due reminders and print them in the console
def check_reminders():
    reminders = load_reminders()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    for reminder in reminders:
        if reminder["time"] == current_time and not reminder["completed"]:
            print(f"\n⏰ Reminder: {reminder['text']} - Due Now!")
            reminder["completed"] = True  # Mark as completed after printing
    save_reminders(reminders)

# Main function to interact with the reminder system
def main():
    while True:
        print("\nReminder Menu:")
        print("1. Add a reminder")
        print("2. List all reminders")
        print("3. Mark a reminder as complete")
        print("4. Delete a reminder")
        print("5. Count reminders")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == "1":
            reminder_text = input("What would you like to be reminded of? ")
            reminder_time = input("Enter the reminder time (YYYY-MM-DD HH:MM): ")
            try:
                # Validate date format
                datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")
                add_reminder(reminder_text, reminder_time)
            except ValueError:
                print("Invalid date format. Please try again.")

        elif choice == "2":
            list_reminders()
            
        elif choice == "3":
            list_reminders()
            index = int(input("Enter the reminder number to mark as complete: ")) - 1
            mark_as_complete(index)
        
        elif choice == "4":
            list_reminders()
            index = int(input("Enter the reminder number to delete: ")) - 1
            delete_reminder(index)

        elif choice == "5":
            count_reminders()

        elif choice == "6":
            print("Exiting the reminder system.")
            break

        else:
            print("Invalid choice. Please try again.")
        
        # Check for reminders every minute
        time.sleep(60)
        check_reminders()

# Run the reminder program
if __name__ == "__main__":
    main()
