## KCK_Project - AI Lunge Technique Analyzer

W pełni interaktywna aplikacja oparta na wizji komputerowej (Computer Vision), zaprojektowana do analizy techniki wykonywania wykroków w czasie rzeczywistym. Projekt łączy nowoczesny interfejs graficzny, analizę obrazu z dwóch kamer, sterowanie głosem oraz lokalną bazę danych do monitorowania postępów treningowych.

## Polecenie do wstawienia w terminal żeby pobrać wszytkie niezbędne pakiety pip do urochomienia programu

```bash
$ pip install -r requirements.txt
```
## Przypadki dobrego i zlego użycia:
✅ Przypadki dobrego użycia (Good Use Cases / Happy Paths)
Idealne warunki kadrowania i oświetlenia
Scenariusz: Użytkownik trenuje w dobrze oświetlonym pomieszczeniu. Kamera (lub obie kamery) jest ustawiona na wysokości pasa/klatki piersiowej w odpowiedniej odległości, tak aby cała sylwetka mieściła się w kadrze (szczególnie nogi i miednica).
Rezultat: Model MediaPipe pewnie wychwytuje punkty kluczowe (landmarks), algorytm OpenCV precyzyjnie oblicza kąty w stawach kolanowych, a licznik powtórzeń działa bez zakłóceń.
Wykorzystanie systemu Multi-Camera do zaawansowanej analityki
Scenariusz: Użytkownik podłącza dwie kamery (np. widok z boku i widok z przodu/pod kątem), co zostało zaplanowane w Twoim Sprint v0.0.3.
Rezultat: System uzyskuje trójwymiarowy obraz postawy użytkownika. Pozwala to na rejestrowanie nie tylko zginania kolan, ale także odchyleń bocznych (np. zapadanie się kolana do wewnątrz), co zapewnia maksymalnie dokładny feedback od asystenta.
Sterowanie głosowe (Hands-free) w cichym, domowym otoczeniu
Scenariusz: Użytkownik uruchamia program, zajmuje pozycję i za pomocą komendy głosowej rozpoczyna trening w cichym pokoju.
Rezultat: Moduł STT (SpeechRecognition) wyraźnie wychwytuje komendy bez fałszywych dopasowań, a moduł TTS (pyttsx3 / gTTS) głośno i w odpowiednim momencie informuje o błędach w postawie, bez konieczności podchodzenia do ekranu czy używania myszy/klawiatury.
Zbieranie i analiza danych o postępach
Scenariusz: Użytkownik regularnie wykonuje wykroki z aplikacją.
Rezultat: Lokalna baza danych (SQLite3) poprawnie gromadzi statystyki błędów i liczbę wykonanych serii, pozwalając na śledzenie postępów treningowych na wykresach lub w historii aplikacji.
❌ Przypadki złego użycia (Bad Use Cases / Edge Cases / Misuse)
Częściowe zasłonięcie ciała lub zła perspektywa (Martwe strefy)
Scenariusz: Użytkownik stoi zbyt blisko kamery (ucięte stopy lub kolana) lub nagrywa się mocno z góry/z dołu. Ewentualnie trening odbywa się w ciemnym pomieszczeniu lub pod światło (silne nasłonecznienie z okna).
Problem: Wizja komputerowa gubi kluczowe punkty szkieletu lub błędnie je interpretuje ("zgaduje"). Prowadzi to do sytuacji, w której aplikacja generuje fałszywe ostrzeżenia głosowe o błędach lub pomija prawidłowe powtórzenia.
Zakłócenia akustyczne (Hałaśliwe środowisko)
Scenariusz: Korzystanie z aplikacji w głośnej publicznej siłowni z grającą w tle muzyką lub rozmowami innych osób.
Problem: Mikrofon zbiera głosy z otoczenia, przez co moduł Speech-to-Text nie jest w stanie rozpoznać komend sterujących. Jednocześnie podpowiedzi głosowe (TTS) o technice stają się niesłyszalne dla użytkownika, co czyni funkcję Hands-free bezużyteczną.
Zbyt luźne lub zlewające się z tłem ubranie
Scenariusz: Użytkownik wykonuje wykroki w bardzo szerokich spodniach dresowych (oversize), ukrywających zarysy nóg, lub w odzieży, której kolor całkowicie zlewa się ze ścianą z tyłu.
Problem: MediaPipe może błędnie zidentyfikować rzeczywiste położenie stawów. Obliczenia kątów w kolanach będą zniekształcone, co całkowicie pozbawi algorytm wartości analitycznej.
Wykonywanie ćwiczeń niezgodnych z przeznaczeniem
Scenariusz: Użytkownik próbuje robić zwykłe przysiady, martwy ciąg lub podskoki, oczekując, że aplikacja "inteligentnie" je przeanalizuje.
Problem: Ponieważ algorytm KCK_Project jest ściśle zaprogramowany na biomechanikę i kąty charakterystyczne dla wykroków (Lunges), system zacznie działać nieprzewidywalnie, spamować błędami lub zapisywać bezużyteczne dane (śmieci) do bazy SQLite3
## Zespół Projektowy i Role

Projekt został zrealizowany w ramach metodyki **Scrum**. Zespół składa się z trzech osób, z wyraźnie podzielonymi obowiązkami:

* **docRonal (Ivan) (Twórca projektu i Scrum Master)** 
  Pomysłodawca projektu. Odpowiedzialny za wdrożenie komend głosowych (STT), modułu Text-to-Speech (TTS), implementację bezdotykowego sterowania aplikacją (hands-free) oraz głęboką refaktoryzację i architekturę kodu.
* **refrigerator2 (Tsimur)(Główny Deweloper / Lead Developer)** 
  Główny projektant i programista interfejsu użytkownika. Odpowiadał za migrację i wdrożenie nowoczesnego GUI w oparciu o CustomTkinter, a także za intensywne debugowanie, optymalizację i bieżącą refaktoryzację aplikacji.
* **YuriiSladkovskyi (Odpowiedzialny za Bazy Danych i Architekt)** 
  Zajął się projektowaniem i wdrożeniem logiki zapisu danych. Odpowiada za integrację lokalnej bazy danych SQLite3, aktualizację stosu technologicznego w kodzie oraz architekturę systemu śledzenia postępów.

## Główne Funkcjonalności

- **Analiza w Czasie Rzeczywistym:** Obliczanie kątów w stawach kolanowych z wykorzystaniem OpenCV.
- **Sterowanie Głosowe (Hands-free):** Pełna nawigacja po aplikacji bez użycia rąk dzięki technologii Speech-to-Text (STT).
- **Asystent Treningowy (TTS):** Głosowe komunikaty o błędach w postawie i automatyczne zliczanie powtórzeń.
- **Wsparcie dla Multi-Camera:** Zwiększona precyzja analizy ruchu poprzez jednoczesną obsługę obrazu z dwóch kamer.
- **Zapis Historii Treningów:** Wbudowana baza danych SQLite3 do śledzenia postępów i statystyk błędów.

## Technologie
- **Język:** Python 3.x
- **Computer Vision:** OpenCV, MediaPipe (do detekcji szkieletu/kątów)
- **GUI:** CustomTkinter
- **Audio/Voice:** Biblioteki STT (SpeechRecognition) oraz TTS (pyttsx3 / gTTS)
- **Baza Danych:** SQLite3

---

## Oś Czasu Projektu (Scrum Sprints)

### Sprint v0.0.1 — Core Prototype & MVP
* **Cel:** Stworzenie funkcjonalnego prototypu (MVP) do analizy techniki wykonywania wykroków w czasie rzeczywistym.
* **Zakres prac:**
  * Opracowanie algorytmu Computer Vision do obliczania kątów w stawach kolanowych.
  * Implementacja bazowego interfejsu wyświetlania obrazu z kamery przy użyciu biblioteki OpenCV.
  * Integracja modułu TTS (Text-to-Speech) do głosowego powiadamiania użytkownika o błędach i instruktażu.
* **Wynik:** Powstał działający prototyp, który automatycznie zlicza powtórzenia ćwiczenia i koryguje błędy użytkownika za pomocą komunikatów głosowych.

### Sprint v0.0.2 — UI/UX & Voice Control
* **Cel:** Modernizacja interfejsu użytkownika oraz wdrożenie bezdotykowego sterowania głosowego.
* **Zakres prac:**
  * Migracja interfejsu graficznego z okna OpenCV na nowoczesny framework CustomTkinter.
  * Implementacja technologii STT (Speech-to-Text) do sterowania aplikacją za pomocą komend głosowych.
  * Głęboka refaktoryzacja kodu w celu poprawy jego czytelności i wydajności.
* **Wynik:** Aplikacja zyskała intuicyjny, nowoczesny design i możliwość sterowania głosem. Zoptymalizowana struktura kodu przygotowała projekt pod dalszy rozwój.

### Sprint v0.0.3 — Data Persistence & Multi-view Analysis
* **Cel:** Implementacja systemu zapisu historii treningów oraz zwiększenie precyzji analizy ruchu dzięki obsłudze dwóch kamer.
* **Zakres prac:**
  * Zaprojektowanie i wdrożenie lokalnej bazy danych opartej na SQLite3.
  * Stworzenie logiki analitycznej do śledzenia postępów użytkownika (statystyki serii, historia błędów).
  * Konfiguracja obsługi dwóch kamer jednocześnie i dostosowanie algorytmu do analizy sylwetki z różnych perspektyw.
* **Wynik:** Użytkownik ma możliwość monitorowania swojego progresu w czasie. Wykorzystanie analizy wielokamerowej znacząco zwiększyło dokładność wykrywania błędów podczas ćwiczeń.
