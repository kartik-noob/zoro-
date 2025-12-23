import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import time
from client import ask_ai
from markdown2speech import markdown_to_speech
import musicLibrary

recognizer = sr.Recognizer()

newsapi = "https://newsapi.org/v2/top-headlines?country=us&apiKey=4c109b3b74f945cab4aa11f2911161ce"


def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    return recognizer.recognize_google(audio)

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    engine.setProperty('rate', 190)  # speech speed aahe hee
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)    
    elif "news" in c:
        r = requests.get(newsapi)
        if r.status_code == 200:
            articles = r.json().get("articles", [])
            for article in articles[:5]:  # limit headlines
                speak(article["title"])
    elif "use ai" in c:
        speak("What's your query?")
        try:
            query = listen()
            print("AI Query:", query)

            speak("Thinking...")
            answer_md = ask_ai(query)
            print("\n=== AI RESPONSE ===\n")
            print(answer_md)
            print("\n==================\n")
            speech_text = markdown_to_speech(answer_md)
            speak(speech_text)

        except sr.UnknownValueError:
            speak("I didn't understand the query.")

    else:
        speak("I don't recognize that command.")            

if __name__ == "__main__":
    speak("Initializing Zoro")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    while True:
        try:
            print("Listening for wake word...")
            with sr.Microphone() as source:
                audio = recognizer.listen(source)

            word = recognizer.recognize_google(audio)
            print("Heard:", word)

            if word.lower() == "zoro":
                speak("Yes")

                with sr.Microphone() as source:
                    print("Zoro active...")
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)
                print("Command:", command)

                processCommand(command)

        except sr.UnknownValueError:
            pass  

        except Exception as e:
            print("Error:", e)
            time.sleep(1)