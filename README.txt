MIAMI + ICON 2026 — PWA v0.6

1. index.html nadal działa jako zwykły przewodnik HTML po otwarciu lokalnie.
2. Funkcje PWA (instalacja na ekranie głównym + service worker/offline cache) wymagają uruchomienia przez HTTPS albo localhost.
3. Najprostsza publikacja: wrzucić cały folder na dowolny statyczny hosting HTTPS (np. GitHub Pages / Netlify / Cloudflare Pages).
4. Po pierwszym otwarciu online wybierz „Dodaj do ekranu głównego” / „Zainstaluj”.
5. Dane planu i interfejs są cache'owane. Google Maps, Uber, Royal, pogoda i oficjalne alerty są celowo LIVE i wymagają internetu.
6. Jeśli aplikacja pokazuje OFFLINE, nadal korzystaj z planu i zapisanych instrukcji; LIVE będzie dostępne po odzyskaniu sieci.
