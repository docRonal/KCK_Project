import speech_recognition as sr
import pyttsx3
from translate import Translator

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak...")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language='en-US')
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError:
            print("Speech service error")
            return ""

text = recognize()

translator = Translator(from_lang="en", to_lang="ru")
translation = translator.translate(text)

print("Translation:", translation)

speak(translation)