MIAMI + ICON 2026 — PWA v0.7.1

CO NOWE
- version.json + sprawdzanie nowej wersji przy połączeniu z internetem
- service worker z network-first dla index.html i version.json
- bezpieczne przejęcie nowego service workera bez reinstalacji aplikacji
- GitHub Actions QA po każdym pushu / PR do main
- scripts/qa.py: wymagane pliki, dni 9–20 XII, warstwy UI, linki wewnętrzne,
  podstawowy secret scan oraz kontrola PWA update hooks

PUBLIKACJA
Repo GitHub Pages:
  montplus-owner/miami-icon-2026-guide

W repo podmień/dodaj całą zawartość tego folderu.
GitHub Pages pozostaje:
  Source: Deploy from a branch
  Branch: main
  Folder: / (root)

Po commicie:
1. Zakładka Actions powinna pokazać workflow "Guide QA".
2. Zielony check = statyczny QA przeszedł.
3. GitHub Pages opublikuje main jak dotychczas.
4. Zainstalowane PWA nie wymaga reinstalacji.
5. Gdy version.json będzie nowszy niż wersja uruchomionej aplikacji,
   pokaże się zielony banner aktualizacji.

WAŻNE
- LIVE, Google Maps, Uber, Royal i pogoda celowo wymagają internetu.
- Nie umieszczaj w publicznym repo numerów rezerwacji, paszportów ani innych danych wrażliwych.

HOTFIX v0.7.1
- Dec20: Government Center → Green Line NORTHBOUND toward Palmetto → Earlington Heights → Orange Airport Shuttle → MIA.
- QA now blocks regression to the wrong southbound instruction.
