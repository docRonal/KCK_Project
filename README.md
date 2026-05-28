# KCK_Project
## Oś czasu projektu (Sprinty)
### Sprint v0.0.1 — Core Prototype & MVP
* **Cel:** Stworzenie funkcjonalnego prototypu (MVP) do analizy techniki wykonywania wykroków w czasie rzeczywistym.
* **Zakres prac:**
  * Opracowanie algorytmu *Computer Vision* do obliczania kątów w stawach kolanowych.
  * Implementacja bazowego interfejsu wyświetlania obrazu z kamery przy użyciu biblioteki `OpenCV`.
  * Integracja modułu **TTS (Text-to-Speech)** do głosowego powiadamiania użytkownika o błędach i instruktażu.
* **Wynik:** Powstał działający prototyp, który automatycznie zlicza powtórzenia ćwiczenia i koryguje błędy użytkownika za pomocą komunikatów głosowych.

---

### Sprint v0.0.2 — UI/UX & Voice Control
* **Cel:** Modernizacja interfejsu użytkownika oraz wdrożenie bezdotykowego sterowania głosowego.
* **Zakres prac:**
  * Migracja interfejsu graficznego z okna OpenCV na nowoczesny framework **CustomTkinter**.
  * Implementacja technologii **STT (Speech-to-Text)** do sterowania aplikacją za pomocą komend głosowych (funkcja *hands-free*).
  * Głęboki refaktoryzacja kodu w celu poprawy jego czytelności i wydajności.
* **Wynik:** Aplikacja zyskała intuicyjny, nowoczesny design i możliwość sterowania głosem. Zoptymalizowana struktura kodu przygotowała projekt pod dalszy rozwój.

---

### Sprint v0.0.3 — Data Persistence & Multi-view Analysis
* **Cel:** Implementacja systemu zapisu historii treningów oraz zwiększenie precyzji analizy ruchu dzięki obsłudze dwóch kamer.
* **Zakres prac:**
  * Zaprojektowanie i wdrożenie lokalnej bazy danych opartej na **SQLite3**.
  * Stworzenie logiki analitycznej do śledzenia postępów użytkownika (statystyki serii, historia błędów).
  * Konfiguracja obsługi **dwóch kamer jednocześnie** i dostosowanie algorytmu do analizy sylwetki z różnych perspektyw.
* **Wynik:** Użytkownik ma możliwość monitorowania swojego progresu w czasie. Wykorzystanie analizy wielokamerowej znacząco zwiększyło dokładność wykrywania błędów podczas ćwiczeń.
