import pyttsx3
import queue
import threading
import time

# Очередь для фраз
speech_queue = queue.Queue()


def _worker():
    """Фоновый поток, который живет всё время работы программы"""
    # Инициализируем движок ОДИН РАЗ внутри этого потока
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)

    while True:
        try:
            # Ждем текст из очереди
            text = speech_queue.get(timeout=1)
            if text is None:
                break  # Сигнал для выхода

            engine.say(text)
            engine.runAndWait()

            # Небольшая пауза, чтобы не захлебываться
            speech_queue.task_done()
        except queue.Empty:
            continue
        except Exception as e:
            print(f"TTS Error: {e}")


# Запускаем поток-воркер один раз при импорте модуля
worker_thread = threading.Thread(target=_worker, daemon=True)
worker_thread.start()


def speak(text):
    """Теперь эта функция просто кидает текст в очередь, что очень быстро"""
    if text:
        speech_queue.put(text)


def stop_tts():
    """Для корректного завершения"""
    speech_queue.put(None)
