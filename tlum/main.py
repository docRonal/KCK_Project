from core import speak, listen, translate_text


def main():
    speak("Powiedz polski lub angielski aby wybrać język", "pl")

    language = "pl"
    while True:
        text = listen()

        if text == "":
            continue

        if "bywaj" in text or "good bye" in text:
            speak("Do widzenia", "pl")
            break

        if "polski" in text:
            language = "pl"
            speak("Ustawiono język polski", "pl")
            continue

        if "angielski" in text:
            language = "en"
            speak("Language changed to English", "en")
            continue

        translation = translate_text(text, language)

        if translation is None:
            speak("Błąd tłumaczenia", "pl")
            continue

        speak("Tłumaczenie:", "pl")
        speak(translation, language)


if __name__ == "__main__":
    main()
