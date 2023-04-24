# PlanDoskonały

## Cel projektu
Co semestr studenci Uniwersytetu Warszawskiego muszą ułożyć plan zajęć. Jest to szczególnie pracochłonne zadanie dla osób, które chcą zminimalizować liczbę kolizji i okienek jednocześnie wybierając preferowanych prowadzących. PlanDoskonały to narzędzie udostępniane w formie strony internetowej, które ma za zadanie ułatwić układanie planu zajęć poprzez proponowanie optymalnego planu użytkownikowi na podstawie algorytmu sparametryzowanego za pomocą przyjaznego interface'u.

## Użytkownicy
Użytkownikami strony będą studenci Uniwersytetu Warszawskiego, w szczególności studenci studiujący na kilku wydziałach na raz, albo dobierający wiele przedmiotów np. studenci MISMaP, MISH, JSIM.

## Funkcjonalność
1. proponowanie optymalnego planu
    - minimalizacja liczby kolizji
    - minimalizacja liczby okienek
    - optymalizacja sumy ocen prowadzących (optional feature)
2. autoryzacja poprzez USOSa UW
3. wyszukiwanie przedmiotów i grup (poprzez skorzystanie z API USOSa UW)
4. zapisywanie planu na swoim koncie
5. optymalizacja sumy ocen prowadzących (optional feature)

## Technologie
- frontend: Vue.js (JavaScript lub TypeScript)
- backend: Django (Python), SQLite