import speech_recognition as r
import pyttsx3

print("--- ДОСТУПНІ МІКРОФОНИ ---")
try:
    mics = r.Microphone.list_microphone_names()
    for index, name in enumerate(mics):
        print(f"ID: {index} -> Назва: {name}")
except Exception as e:
    print(f"Помилка мікрофона: {e}")

print("\n--- ДОСТУПНІ ГОЛОСИ TTS ---")
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"ID: {voice.id} -> Ім'я: {voice.name} -> Мови: {getattr(voice, 'languages', 'Не вказано')}")
except Exception as e:
    print(f"Помилка TTS: {e}")