import pyttsx3
import queue
import threading

speech_queue = queue.Queue()

def _init_engine():
    """Допоміжна функція для створення та налаштування рушія."""
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    
    # Шукаємо польський голос
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'PAULINA' in voice.id.upper() or 'pl-PL' in getattr(voice, 'languages', []):
            engine.setProperty('voice', voice.id)
            break
            
    return engine

def _worker():
    try:
        # Перший тестовий запуск
        engine = _init_engine()
        engine.say("System audio gotowy")
        engine.runAndWait()
        del engine # Важливо звільнити ресурси рушія після використання
        
        while True:
            try:
                text = speech_queue.get(timeout=1)
                if text is None:
                    break 

                engine = _init_engine()
                engine.say(text)
                engine.runAndWait()
                del engine
                
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
    print(f"TTS Request: {text}")
    if text:
        speech_queue.put(text)

def stop_tts():
    speech_queue.put(None)