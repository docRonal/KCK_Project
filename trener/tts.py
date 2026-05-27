import pyttsx3
import threading

is_speaking = False


def tts_task(text):
    global is_speaking
    try:
        import pythoncom

        pythoncom.CoInitialize()
    except ImportError:
        pass

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Audio Error: {e}")
    finally:
        is_speaking = False


def speak(text):
    global is_speaking
    if not is_speaking:
        is_speaking = True
        threading.Thread(target=tts_task, args=(text,), daemon=True).start()
