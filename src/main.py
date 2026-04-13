"""
Command line runner for the Music Recommender Simulation.
"""
from src.recommender import load_songs, recommend_songs

def print_recommendations(profile_name: str, recommendations: list) -> None:
    """Prints recommendations in a clean, readable format."""
    print(f"\n{'='*50}")
    print(f"Profile: {profile_name}")
    print(f"{'='*50}")
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"\n#{i} {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f}")
        print(f"    Why   : {explanation}")
    print()

def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # --- Profile 1: High Energy Pop ---
    high_energy_pop = {
        "genre": "pop",
        "mood": "happy",
        "target_energy": 0.9,
        "target_valence": 0.85,
        "target_danceability": 0.85,
        "target_acousticness": 0.2,
        "target_tempo": 130
    }

    # --- Profile 2: Chill Lofi ---
    chill_lofi = {
        "genre": "lofi",
        "mood": "chill",
        "target_energy": 0.2,
        "target_valence": 0.5,
        "target_danceability": 0.3,
        "target_acousticness": 0.8,
        "target_tempo": 75
    }

    # --- Profile 3: Deep Intense Rock ---
    deep_rock = {
        "genre": "rock",
        "mood": "intense",
        "target_energy": 0.95,
        "target_valence": 0.4,
        "target_danceability": 0.5,
        "target_acousticness": 0.1,
        "target_tempo": 155
    }

    # --- Profile 4: Adversarial (conflicting preferences) ---
    adversarial = {
        "genre": "pop",
        "mood": "sad",
        "target_energy": 0.9,
        "target_valence": 0.2,
        "target_danceability": 0.9,
        "target_acousticness": 0.9,
        "target_tempo": 140
    }

    # --- Run all profiles ---
    profiles = [
        ("High Energy Pop",        high_energy_pop),
        ("Chill Lofi",             chill_lofi),
        ("Deep Intense Rock",      deep_rock),
        ("Adversarial (conflicting)", adversarial),
    ]

    for name, prefs in profiles:
        recs = recommend_songs(prefs, songs, k=5)
        print_recommendations(name, recs)

if __name__ == "__main__":
    main()

