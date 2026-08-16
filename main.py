import pyttsx3 
import datetime
import speech_recognition as sr
import webbrowser
import os
import time

# --- Voice Engine Setup ---
def get_engine():
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) # 0 mard, 1 larki
    engine.setProperty('rate', 170)
    return engine

def speak(audio):
    print(f"Jarvis: {audio}")
    temp_engine = get_engine()
    temp_engine.say(audio)
    temp_engine.runAndWait()
    temp_engine.stop()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Boss!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Boss!")
    else:
        speak("Good Evening Boss!")
    speak("Jarvis is online. Aaj kya kaam karna hai?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception:
        return "none"
    return query.lower()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        # --- 1. GOOGLE SEARCH (Wikipedia ka behtareen badal) ---
        if 'search' in query:
            speak('Searching on Google...')
            query = query.replace("search", "")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Boss, maine Google par {query} dhoond liya hai.")

        # --- 2. YOUTUBE ---
        elif 'open youtube' in query:
            speak("Ji Boss, YouTube khol raha hoon.")
            webbrowser.open("https://www.youtube.com")

        # --- 3. WHATSAPP ---
        elif 'open whatsapp' in query:
            speak("Theek hai Boss, WhatsApp Web hazir hai. Scan kar lein.")
            webbrowser.open("https://web.whatsapp.com")

        # --- 4. NOTEPAD ---
        elif 'open notepad' in query:
            speak("Notepad open kar raha hoon.")
            os.startfile('notepad.exe')

        # --- 5. TIME ---
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")    
            speak(f"Boss, waqt ho raha hai {strTime}")

        # --- 6. EXIT ---
        elif 'exit' in query or 'stop' in query:
            speak("Allah Hafiz Boss! Jab zaroorat ho bula lijiyega.")
            break