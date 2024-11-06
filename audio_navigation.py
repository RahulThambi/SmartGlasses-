import googlemaps
import pyttsx3
import time
from geopy.distance import geodesic
import geocoder
import sys
import requests

# Initialize Google Maps client
gmaps = googlemaps.Client(key='AIzaSyBrNK24Z49Uqn7qfQGO42jU-0-ZV9adpjo') # https://console.cloud.google.com/google/maps-apis/credentials?project=artful-affinity-432106-n0

# Initialize text-to-speech engine
engine = pyttsx3.init()

def get_current_location(api_key):
    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=' + api_key
    response = requests.post(url, json={})
    location = response.json().get('location')
    if location:
        return f"{location['lat']},{location['lng']}"
    else:
        return None

def get_directions(origin, destination):
    try:
        directions = gmaps.directions(origin, destination, mode="walking")
        if not directions:
            raise ValueError("No directions found. Please check the destination and try again.")
        return directions[0]['legs'][0]['steps']
    except googlemaps.exceptions.ApiError as e:
        print(f"API error: {e}")
        return None
    except ValueError as e:
        print(e)
        return None

def speak(text):
    engine.say(text)
    engine.runAndWait()

def print_and_speak(text):
    print(text)
    speak(text)

def calculate_estimated_time_and_distance(origin, destination):
    directions = gmaps.directions(origin, destination, mode="walking")
    if not directions:
        return None, None
    leg = directions[0]['legs'][0]
    distance = leg['distance']['text']
    duration = leg['duration']['text']
    return distance, duration

def navigate(destination):
    api_key = 'AIzaSyBrNK24Z49Uqn7qfQGO42jU-0-ZV9adpjo'
    origin = get_current_location(api_key)
    if not origin:
        print_and_speak("Unable to determine current location.")
        return

    distance, duration = calculate_estimated_time_and_distance(origin, destination)
    if distance and duration:
        print_and_speak(f"Your destination is {distance} away and it will take approximately {duration} to get there.")
    else:
        print_and_speak("Unable to calculate distance and duration.")
        return

    steps = get_directions(origin, destination)
    if not steps:
        print_and_speak("Unable to find directions.")
        return

    print_and_speak(f"Starting navigation from your current location to {destination}")

    # Collect and print all steps together before starting navigation
    all_instructions = []
    for i, step in enumerate(steps):
        instruction = step['html_instructions'].replace('<b>', '').replace('</b>', '').replace('<div style="font-size:0.9em">', '. ').replace('</div>', '')
        all_instructions.append(f"Step {i+1}: {instruction}")

    # Print all instructions at once
    full_directions = "\n".join(all_instructions)
    print(full_directions)
    #speak(full_directions)

    for i, step in enumerate(steps):
        instruction = step['html_instructions'].replace('<b>', '').replace('</b>', '').replace('<div style="font-size:0.9em">', '. ').replace('</div>', '')
        step_distance = geodesic(
            (step['start_location']['lat'], step['start_location']['lng']),
            (step['end_location']['lat'], step['end_location']['lng'])
        ).meters
        step_duration = step['duration']['text']
        print_and_speak(f"Step {i+1}: {instruction}. Walk for {step_distance:.2f} meters, approximately {step_duration}")


        # Wait until user reaches the start location of the next step
        while True:
            current_location = get_current_location(api_key)
            if not current_location:
                print_and_speak("Unable to determine current location.")
                return

            # Calculate the distance between the current location and the next step's start location
            distance_to_next_step = geodesic(current_location, (step['start_location']['lat'], step['start_location']['lng'])).meters

            # Proceed to the next instruction if the user is within 10 meters of the next step's start location
            if distance_to_next_step < 10:
                break

            # Check location every 5 seconds
            time.sleep(5)

        # Simulate walking from the current step's start to end location
        start_location = (step['start_location']['lat'], step['start_location']['lng'])
        end_location = (step['end_location']['lat'], step['end_location']['lng'])
        distance = geodesic(start_location, end_location).meters

        # Simulate walking at 1.4 meters per second
        walking_time = distance / 1.4
        time.sleep(min(walking_time, 5))  # Cap waiting time at 5 seconds for demonstration

    print_and_speak("You have reached your destination.")

if __name__ == "__main__":
    destination = sys.argv[2]
    navigate(destination)
