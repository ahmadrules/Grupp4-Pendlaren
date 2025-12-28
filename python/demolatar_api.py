#demolatar_api.py
import requests

BASE_URL = "https://www.demolatar.se/api"

class DemolatarAPI:
    """Enkel klient för demolatar.se API."""

    def __init__(self, timeout=10):
        self.timeout = timeout

    def get_latest_tracks(self, n=10):
        url = f"{BASE_URL}/getLatestTracks.php"
        params = {"q": n}
        r = requests.get(url, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def get_random_track(self):
        url = f"{BASE_URL}/getRandomTrack.php"
        r = requests.get(url, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def search(self, query):
        """Söker i demolåtarnas databas (band, låtar, genre)."""
        url = f"{BASE_URL}/search.php"
        params = {"q": query}
        r = requests.get(url, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    # --------------------------------------------
    #hämta låtar efter genre
    # --------------------------------------------
    def get_tracks_by_genre(self, genre, limit=20):
        """
        Hämtar låtar baserat på genre (via search-endpoint).
        Exempel: genre="metal", "punk", "electronic".
        """
        results = self.search(genre)

        #api kan returnera en lista eller ett objekt
        if not isinstance(results, list):
            return []

        #begränsa antalet låtar
        return results[:limit]

    #spellista baserat på restid + genre
    def get_playlist_for_duration_and_genre(self, minutes_left, genre, avg_length=3.5):
        """
        Skapar en genrebaserad spellista anpassad efter restiden.
        """
        if minutes_left <= 0:
            return []

        #hur många låtar behövs? (ungefär)
        count = max(1, int(minutes_left / avg_length))
        count = min(count, 50)  # API begränsning

        #hämta låtar i vald genre
        genre_tracks = self.get_tracks_by_genre(genre, limit=count)

        return genre_tracks
