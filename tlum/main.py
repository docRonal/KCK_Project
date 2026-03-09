import speech_recognition as sr
import pyttsx3
import webbrowser
from translate import Translator

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def recognize(msg = "something"):
    r = sr.Recognizer()
