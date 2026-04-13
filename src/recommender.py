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


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences using the algorithm recipe."""
    score = 0.0
    reasons = []

    # Genre match — 50 points
    if song["genre"] == user_prefs.get("genre"):
        score += 50
        reasons.append("genre match (+50)")

    # Mood match — 30 points
    if song["mood"] == user_prefs.get("mood"):
        score += 30
        reasons.append("mood match (+30)")

    # Energy proximity — up to 8 points
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

    # Valence proximity — up to 6 points
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

    # Danceability proximity — up to 6 points
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

    # Popularity bonus — up to 5 points
    if song["popularity"] >= 85:
        score += 5
        reasons.append("highly popular (+5)")
    elif song["popularity"] >= 70:
        score += 3
        reasons.append("moderately popular (+3)")

    # Mood tag bonus — up to 4 points
    if song["mood_tag"] == user_prefs.get("mood_tag"):
        score += 4
        reasons.append(f"mood tag match (+4)")

    return (score, reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores all songs, sorts by score, and returns the top k recommendations."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))

    # sorted() returns a new list without modifying original
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
