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
        "target_tempo": 130,
        "mood_tag": "euphoric"
    }

    # --- Profile 2: Chill Lofi ---
    chill_lofi = {
        "genre": "lofi",
        "mood": "chill",
        "target_energy": 0.2,
        "target_valence": 0.5,
        "target_danceability": 0.3,
        "target_acousticness": 0.8,
        "target_tempo": 75,
        "mood_tag": "serene"
    }

    # --- Profile 3: Deep Intense Rock ---
    deep_rock = {
        "genre": "rock",
        "mood": "intense",
        "target_energy": 0.95,
        "target_valence": 0.4,
        "target_danceability": 0.5,
        "target_acousticness": 0.1,
        "target_tempo": 155,
        "mood_tag": "aggressive"
    }

    # --- Profile 4: Adversarial (conflicting preferences) ---
    adversarial = {
        "genre": "pop",
        "mood": "sad",
        "target_energy": 0.9,
        "target_valence": 0.2,
        "target_danceability": 0.9,
        "target_acousticness": 0.9,
        "target_tempo": 140,
        "mood_tag": "melancholic"
    }

    # --- Run all profiles with default mode ---
    profiles = [
        ("High Energy Pop",           high_energy_pop),
        ("Chill Lofi",                chill_lofi),
        ("Deep Intense Rock",          deep_rock),
        ("Adversarial (conflicting)",  adversarial),
    ]

    for name, prefs in profiles:
        recs = recommend_songs(prefs, songs, k=5)
        print_recommendations(name, recs)

    # --- Challenge 2: Scoring Mode Comparison ---
    print("\n" + "="*50)
    print("SCORING MODE COMPARISON — High Energy Pop")
    print("="*50)

    for mode in ["default", "genre_first", "mood_first", "energy_focused"]:
        recs = recommend_songs(high_energy_pop, songs, k=3, mode=mode)
        print(f"\n--- Mode: {mode} ---")
        for i, rec in enumerate(recs, 1):
            song, score, explanation = rec
            print(f"#{i} {song['title']} | Score: {score:.2f}")
            print(f"    {explanation}")


if __name__ == "__main__":
    main()
