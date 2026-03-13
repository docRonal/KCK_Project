import speech_recognition as sr
from translate import Translator
import pyttsx3

engine = pyttsx3.init()

recognizer = sr.Recognizer()


def speak(text, language):
    print(text)
    voices = engine.getProperty("voices")

    if not voices:
        engine.say(text)
        engine.runAndWait()
        return

    for voice in voices:
        langs = voice.languages

        for l in langs:
            lang = str(l).lower()

            if language in lang:
                engine.setProperty("voice", voice.id)
                break
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("Słucham...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="pl-PL")
            print("Powiedziałeś:", text)
            return text.lower()
        except:
            speak("Nie rozumiem", "pl")
            return ""


def translate_text(text, lang):
    if lang == "pl":
        translator = Translator(from_lang="pl", to_lang="en")
    else:
        translator = Translator(from_lang="en", to_lang="pl")

    try:
        result = translator.translate(text)
        return result
    except:
        return None
