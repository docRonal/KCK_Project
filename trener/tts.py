import pyttsx3
import queue
import threading
import time

speech_queue = queue.Queue()

def _worker():
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        
        # Надійно шукаємо Paulina (ми знаємо, що вона є)
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'PAULINA' in voice.id.upper() or 'pl-PL' in getattr(voice, 'languages', []):
                engine.setProperty('voice', voice.id)
                break
                
        # Тестовий звук при запуску (щоб ти знав, що TTS живий)
        engine.say("System audio gotowy")
        engine.runAndWait()

        while True:
            try:
                text = speech_queue.get(timeout=1)
                if text is None:
                    break 

                engine.say(text)
                engine.runAndWait()
                speech_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"TTS Loop Error: {e}")
                
    except Exception as e:
        print(f"CRITICAL TTS INIT ERROR: {e}")

worker_thread = threading.Thread(target=_worker, daemon=True)
worker_thread.start()

def speak(text):
    if text:
        speech_queue.put(text)

def stop_tts():
    speech_queue.put(None)