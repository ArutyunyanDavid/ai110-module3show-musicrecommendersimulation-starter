"""
Command line runner for the Music Recommender Simulation.

This file runs several user profiles so I can compare how the recommender
behaves for different music tastes.

Run it from the project root with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# User profiles to test.
# The first three are "normal" tastes. The last two are tricky "edge case"
# profiles that ask for unusual or conflicting things.
# ---------------------------------------------------------------------------
high_energy_pop = {
    "name": "High-Energy Pop",
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.9,
    "target_valence": 0.9,
    "target_tempo_bpm": 125,
}

chill_lofi = {
    "name": "Chill Lofi",
    "favorite_genre": "lofi",
    "favorite_mood": "calm",
    "target_energy": 0.3,
    "target_valence": 0.5,
    "target_tempo_bpm": 80,
}

deep_intense_rock = {
    "name": "Deep Intense Rock",
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.9,
    "target_valence": 0.4,
    "target_tempo_bpm": 140,
}

# Edge case 1: asks for two things that usually don't go together
# (sad mood is usually low energy, but this user wants high energy).
sad_but_high_energy = {
    "name": "Sad But High Energy",
    "favorite_genre": "pop",
    "favorite_mood": "sad",
    "target_energy": 0.9,
    "target_valence": 0.2,
    "target_tempo_bpm": 130,
}

# Edge case 2: a genre that barely exists in our small dataset.
genre_mismatch_test = {
    "name": "Genre Mismatch Test",
    "favorite_genre": "classical",
    "favorite_mood": "happy",
    "target_energy": 0.8,
    "target_valence": 0.9,
    "target_tempo_bpm": 120,
}

PROFILES = [
    high_energy_pop,
    chill_lofi,
    deep_intense_rock,
    sad_but_high_energy,
    genre_mismatch_test,
]


def print_profile_results(profile: dict, songs: list) -> None:
    """Print one profile's preferences and its top 5 recommendations."""
    print("=" * 40)
    print(f"Profile: {profile['name']}")
    print("Preferences:")
    print(f"Genre: {profile['favorite_genre']}")
    print(f"Mood: {profile['favorite_mood']}")
    print(f"Target Energy: {profile['target_energy']}")
    print(f"Target Valence: {profile['target_valence']}")
    print(f"Target Tempo: {profile['target_tempo_bpm']} BPM")
    print()
    print("Top 5 Recommendations:\n")

    recommendations = recommend_songs(profile, songs, k=5)
    for position, rec in enumerate(recommendations, start=1):
        song = rec["song"]
        print(f"{position}. {song['title']}")
        print(f"Score: {rec['score']:.2f}")
        print("Reasons:")
        for reason in rec["reasons"]:
            print(f"- {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for profile in PROFILES:
        print_profile_results(profile, songs)


if __name__ == "__main__":
    main()
