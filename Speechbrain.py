import speech_recognition as sr
import pyttsx3
import time
import numpy as np
import noisereduce as nr
import requests
import os
from googleapiclient.discovery import build

# Initialize recognizer class and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Your YouTube API key (if needed)
YOUTUBE_API_KEY = 'AIzaSyAx-aQnl7q0sOcgqlrXwo0rNwB_tsJNsio'
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Your Weather API key and endpoint
WEATHER_API_KEY = 'rmkzLhw0SlS3nKqDBmELTIQ9oSXFaa0L'
WEATHER_URL = 'https://api.tomorrow.io/v4/timelines'

# List of exit phrases
exit_phrases = [
    "bye", "goodbye", "see you later", "later", "catch you later",
    "take care", "farewell", "until next time", "peace out", "I'm off"
]

def get_weather(location):
    params = {
        'location': location,
        'fields': 'temperature,precipitationType',
        'units': 'metric',
        'apikey': WEATHER_API_KEY,
    }
    response = requests.get(WEATHER_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data['data']['timelines'][0]['intervals'][0]['values']['temperature']
        precipitation = data['data']['timelines'][0]['intervals'][0]['values']['precipitationType']
        return f"The current temperature in {location} is {temperature}°C with {precipitation}."
    else:
        return "Sorry, I couldn't fetch the weather information."

def get_greeting():
    current_hour = time.localtime().tm_hour  # Get current hour (24-hour format)
    if current_hour < 12:
        return "Good morning!"
    elif 12 <= current_hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

def recognize_speech_from_mic():
    sleeping = False

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")

        while True:
            if not sleeping:
                try:
                    print("Listening for your command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    print("Audio has been recorded.")

                    audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                    reduced_noise = nr.reduce_noise(y=audio_data, sr=source.SAMPLE_RATE)
                    cleaned_audio = sr.AudioData(reduced_noise.tobytes(), source.SAMPLE_RATE, audio.sample_width)

                    text = recognizer.recognize_google(cleaned_audio)
                    print("You said: " + text)

                    if text.lower() == "hello boys":
                        response = f"{get_greeting()} Master, what can I do for you?"
                        print(response)
                        tts_engine.say(response)
                        tts_engine.runAndWait()

                    elif text.lower() == "go to sleep":
                        print("Going to sleep...")
                        tts_engine.say("Going to sleep...")
                        tts_engine.runAndWait()
                        sleeping = True

                    elif any(keyword in text.lower() for keyword in ["weather", "climate"]):
                        tts_engine.say("What location do you want the weather for?")
                        tts_engine.runAndWait()

                        print("Listening for the location...")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        location_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                        reduced_location_noise = nr.reduce_noise(y=location_data, sr=source.SAMPLE_RATE)
                        cleaned_location_audio = sr.AudioData(reduced_location_noise.tobytes(), source.SAMPLE_RATE, audio.sample_width)

                        location_name = recognizer.recognize_google(cleaned_location_audio)
                        print("You said: " + location_name)

                        weather_info = get_weather(location_name)
                        print(weather_info)
                        tts_engine.say(weather_info)
                        tts_engine.runAndWait()

                    elif any(phrase in text.lower() for phrase in ["close redmine", "redmine close", "close issues"]):
                        print("Closing Redmine issues...")
                        os.startfile(r'V:\Projects\VoiceAssistant\Redmine_Close.py')
                        tts_engine.say("Closing Redmine issues now.")
                        tts_engine.runAndWait()

                    elif any(phrase in text.lower() for phrase in exit_phrases):
                        response = "Goodbye! Have a great day!"
                        print(response)
                        tts_engine.say(response)
                        tts_engine.runAndWait()
                        break

                    else:
                        print("Sorry, I didn't catch that.")

                except sr.UnknownValueError:
                    print("Sorry, I didn't catch that.")

                except sr.WaitTimeoutError:
                    print("No input detected. Waiting...")

                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                    time.sleep(5)

            else:
                try:
                    print("Listening for wake word...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                except sr.UnknownValueError:
                    pass

                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                    time.sleep(5)

# Call the function
recognize_speech_from_mic()
