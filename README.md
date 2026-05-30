## KCK_Project - AI Lunge Technique Analyzer

W pełni interaktywna aplikacja oparta na wizji komputerowej (Computer Vision), zaprojektowana do analizy techniki wykonywania wykroków w czasie rzeczywistym. Projekt łączy nowoczesny interfejs graficzny, analizę obrazu z dwóch kamer, sterowanie głosem oraz lokalną bazę danych do monitorowania postępów treningowych.

## Zespół Projektowy i Role

Projekt został zrealizowany w ramach metodyki **Scrum**. Zespół składa się z trzech osób, z wyraźnie podzielonymi obowiązkami:

* **docRonal (Twórca projektu i Scrum Master)** 
  Pomysłodawca projektu. Odpowiedzialny za wdrożenie komend głosowych (STT), modułu Text-to-Speech (TTS), implementację bezdotykowego sterowania aplikacją (hands-free) oraz głęboką refaktoryzację i architekturę kodu.
* **refrigerator2 (Główny Deweloper / Lead Developer)** 
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
