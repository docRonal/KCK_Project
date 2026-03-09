import speech_recognition as sr
from translate import Translator
import pyttsx3

engine = pyttsx3.init()

recognizer = sr.Recognizer()

language = "pl"


def speak(text):
    print(text)
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
            speak("Nie rozumiem")
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


speak("Powiedz polski lub angielski aby wybrać język")

while True:

    text = listen()

    if text == "":
        continue

    if "bywaj" in text or "good bye" in text:
        speak("Do widzenia")
        break

    if "polski" in text:
        language = "pl"
        speak("Ustawiono język polski")
        continue

    if "angielski" in text:
        language = "en"
        speak("Language changed to English")
        continue

    translation = translate_text(text, language)

    if translation is None:
        speak("Błąd tłumaczenia")
        continue

    speak("Tłumaczenie:")
    speak(translation)