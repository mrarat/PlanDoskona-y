# Wymagania niefunkcjonalne
### Dostępność
Strona internetowa ma być dostępna przez >90% czasu. Pozostałe 10% jest rezerwowane na przerwy techniczne i problemy, które mogą wystąpić. Dodatkowo można założyć, że użytkownicy w trakcie godzin nocnych nie będą korzystać ze strony. Okresowy brak dostępności nie powinien być również wielkim problemem dla użytkowników, jako że strona nie udostępnia krytycznych funkcjonalności.

### Przenośność
Strona jest dostępna na wszystkich urządzeniach umożliwiających korzystanie z przeglądarki internetowej. Natomiast jest ona zoptymalizowana pod kątem komputerów osobistych.

### Pojemność bazy danych
Baza danych przechowuje dane statystyczne na temat popularności grup. Można oszacować, że dane dla 1 grupy zajęciowej zamują około 100 B. Średnio przedmiot posiada 5 grup zajęciowych. Na jednym wydziale jest średnio 550 przedmiotów. Uniwersytet Warszawski posiada 25 wydziałów. Na podstawie tych informacji przy założeniu, że w bazie danych będą przechowywane statystyki dla wszystkich grup i przedmiotów, można zgrubnie oszacować pojemność bazy danych na 100 B * 5 * 550 * 25 = 6,875 MB.

### Wydajność
Ilość użytkowników jest ograniczona ze względu na to, że docelową grupą użytkowników są studenci UW. Według danych (https://www.uw.edu.pl/uniwersytet/fakty-i-liczby//) możemy oszacować od góry liczbę studentów na 40 000. Jeśli założymy, że studenci potrzebują układać plan 2 razy do roku to możemy spodziewać się znikomego ruchu. Ponieważ strona internetowa jest w formacie SPA, to jedyne obciążenie dla serwera to hostowanie plików strony (które są ładowane tylko raz) oraz przyjmowanie statystyk po wygenerowaniu planu. Algorytm optymalizujący plan będzie wykorzystywał moc obliczeniową komputera użytkownika. Tym samym sumarycznie obciążenie serwera powinno być minimalne - przez znaczną większość czasu poniżej kilku requestów na sekundę.