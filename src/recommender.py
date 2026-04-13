from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """OOP implementation of the recommendation logic."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns top k songs ranked by score for the given user."""
        scored = []
        for song in self.songs:
            score = 0
            if song.genre == user.favorite_genre:
                score += 50
            if song.mood == user.favorite_mood:
                score += 30
            energy_diff = abs(song.energy - user.target_energy)
            if energy_diff <= 0.1:
                score += 8
            elif energy_diff <= 0.2:
                score += 4
            elif energy_diff <= 0.3:
                score += 2
            if user.likes_acoustic and song.acousticness > 0.7:
                score += 5
            scored.append((score, song))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explains why a song was recommended for a user."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append("genre match (+50)")
        if song.mood == user.favorite_mood:
            reasons.append("mood match (+30)")
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff <= 0.1:
            reasons.append("energy very close (+8)")
        elif energy_diff <= 0.2:
            reasons.append("energy close (+4)")
        elif energy_diff <= 0.3:
            reasons.append("energy somewhat close (+2)")
        if user.likes_acoustic and song.acousticness > 0.7:
            reasons.append("acoustic preference match (+5)")
        return ", ".join(reasons) if reasons else "no strong matches"


def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file and returns a list of dictionaries."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            row["speechiness"] = float(row["speechiness"])
            row["instrumentalness"] = float(row["instrumentalness"])
            row["popularity"] = int(row["popularity"])
            songs.append(row)
    return songs


# --- Scoring Mode Strategies ---
# Each mode applies different weights to prioritize
# different aspects of the user's preferences.

def _score_genre_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Genre-First mode: genre worth 70 points, mood 20, numerics reduced."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += 70
        reasons.append("genre match (+70)")

    if song["mood"] == user_prefs.get("mood"):
        score += 20
        reasons.append("mood match (+20)")

    energy_diff = abs(song["energy"] - user_prefs.get("target_energy", 0.5))
    if energy_diff <= 0.1:
        score += 5
        reasons.append("energy very close (+5)")
    elif energy_diff <= 0.2:
        score += 2
        reasons.append("energy close (+2)")

    if song["popularity"] >= 85:
        score += 5
        reasons.append("highly popular (+5)")
    elif song["popularity"] >= 70:
        score += 3
        reasons.append("moderately popular (+3)")

    if song["mood_tag"] == user_prefs.get("mood_tag"):
        score += 2
        reasons.append("mood tag match (+2)")

    return (score, reasons)


def _score_mood_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Mood-First mode: mood worth 60 points, genre 20, numerics boosted."""
    score = 0.0
    reasons = []

    if song["mood"] == user_prefs.get("mood"):
        score += 60
        reasons.append("mood match (+60)")

    if song["genre"] == user_prefs.get("genre"):
        score += 20
        reasons.append("genre match (+20)")

    energy_diff = abs(song["energy"] - user_prefs.get("target_energy", 0.5))
    if energy_diff <= 0.1:
        score += 8
        reasons.append("energy very close (+8)")
    elif energy_diff <= 0.2:
        score += 4
        reasons.append("energy close (+4)")
    elif energy_diff <= 0.3:
        score += 2
        reasons.append("energy somewhat close (+2)")

    valence_diff = abs(song["valence"] - user_prefs.get("target_valence", 0.5))
    if valence_diff <= 0.1:
        score += 8
        reasons.append("valence very close (+8)")
    elif valence_diff <= 0.2:
        score += 4
        reasons.append("valence close (+4)")

    if song["mood_tag"] == user_prefs.get("mood_tag"):
        score += 4
        reasons.append("mood tag match (+4)")

    return (score, reasons)


def _score_energy_focused(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Energy-Focused mode: energy worth up to 40 points, genre/mood reduced."""
    score = 0.0
    reasons = []

    energy_diff = abs(song["energy"] - user_prefs.get("target_energy", 0.5))
    if energy_diff <= 0.05:
        score += 40
        reasons.append("energy perfect match (+40)")
    elif energy_diff <= 0.1:
        score += 30
        reasons.append("energy very close (+30)")
    elif energy_diff <= 0.2:
        score += 20
        reasons.append("energy close (+20)")
    elif energy_diff <= 0.3:
        score += 10
        reasons.append("energy somewhat close (+10)")

    dance_diff = abs(song["danceability"] - user_prefs.get("target_danceability", 0.5))
    if dance_diff <= 0.1:
        score += 15
        reasons.append("danceability very close (+15)")
    elif dance_diff <= 0.2:
        score += 8
        reasons.append("danceability close (+8)")

    if song["genre"] == user_prefs.get("genre"):
        score += 15
        reasons.append("genre match (+15)")

    if song["mood"] == user_prefs.get("mood"):
        score += 10
        reasons.append("mood match (+10)")

    if song["popularity"] >= 85:
        score += 5
        reasons.append("highly popular (+5)")
    elif song["popularity"] >= 70:
        score += 3
        reasons.append("moderately popular (+3)")

    return (score, reasons)


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song using the default balanced algorithm recipe."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += 50
        reasons.append("genre match (+50)")

    if song["mood"] == user_prefs.get("mood"):
        score += 30
        reasons.append("mood match (+30)")

    energy_diff = abs(song["energy"] - user_prefs.get("target_energy", 0.5))
    if energy_diff <= 0.1:
        score += 8
        reasons.append("energy very close (+8)")
    elif energy_diff <= 0.2:
        score += 4
        reasons.append("energy close (+4)")
    elif energy_diff <= 0.3:
        score += 2
        reasons.append("energy somewhat close (+2)")

    valence_diff = abs(song["valence"] - user_prefs.get("target_valence", 0.5))
    if valence_diff <= 0.1:
        score += 6
        reasons.append("valence very close (+6)")
    elif valence_diff <= 0.2:
        score += 3
        reasons.append("valence close (+3)")
    elif valence_diff <= 0.3:
        score += 1
        reasons.append("valence somewhat close (+1)")

    dance_diff = abs(song["danceability"] - user_prefs.get("target_danceability", 0.5))
    if dance_diff <= 0.1:
        score += 6
        reasons.append("danceability very close (+6)")
    elif dance_diff <= 0.2:
        score += 3
        reasons.append("danceability close (+3)")
    elif dance_diff <= 0.3:
        score += 1
        reasons.append("danceability somewhat close (+1)")

    if song["popularity"] >= 85:
        score += 5
        reasons.append("highly popular (+5)")
    elif song["popularity"] >= 70:
        score += 3
        reasons.append("moderately popular (+3)")

    if song["mood_tag"] == user_prefs.get("mood_tag"):
        score += 4
        reasons.append("mood tag match (+4)")

    return (score, reasons)


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "default"
) -> List[Tuple[Dict, float, str]]:
    """
    Scores all songs and returns top k recommendations.
    Mode options: 'default', 'genre_first', 'mood_first', 'energy_focused'
    """
    # Pick scoring strategy based on mode
    mode_map = {
        "default":        score_song,
        "genre_first":    _score_genre_first,
        "mood_first":     _score_mood_first,
        "energy_focused": _score_energy_focused,
    }
    scoring_fn = mode_map.get(mode, score_song)

    scored = []
    for song in songs:
        score, reasons = scoring_fn(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))

    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
