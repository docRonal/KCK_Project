import speech_recognition as sr
import threading
from tts import speak

class VoiceAssistant:
    def __init__(self, state):
        self.state = state
        self.recognizer = sr.Recognizer()
        self.is_listening = True

    def listen_loop(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Mikrofon gotowy. Słucham...")
            
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=4)
                    
                    command = self.recognizer.recognize_google(audio, language="pl-PL").lower()
                    print(f"Rozpoznano: {command}")
                    self.process_command(command)
                    
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    print(f"Błąd mikrofonu: {e}")

    def process_command(self, command):
        if "trening" in command or "start" in command:
            self.state["is_training"] = True
            speak("Start trening")
            
        elif "zakończ" in command or "koniec" in command:
            self.state["is_training"] = False
            self.state["quit"] = True 
            speak("The End")
            
        elif "ile powtórzeń" in command or "ile" in command:
            if self.state.get("is_training"):
                reps = self.state.get("reps", 0)
                speak(f"You {reps} reapites")
            else:
                speak("Training is not start")
                
        elif "ile zostało" in command:
            if self.state.get("is_training"):
                target = self.state.get("target_reps", 10) 
                reps = self.state.get("reps", 0)
                left = target - reps
                if left > 0:
                    speak(f"Zostało {left} powtórzeń")
                else:
                    speak("Goal!")
            else:
                speak("Trening is not start")

    def start(self):
        thread = threading.Thread(target=self.listen_loop, daemon=True)
        thread.start()