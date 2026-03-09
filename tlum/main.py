import speech_recognition as sr
import pyttsx3
import webbrowser
from translate import Translator

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def recognize(msg = "something"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            recognised_text = r.recognize_google (audio, language='en-US')
            print(recognised_text)
            return recognised_text.lower()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}",e)

text = recognize()
word_list = text.split()
translator = Translator()

