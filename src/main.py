"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

Run it from the project root with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    # 1) Load the songs from the CSV file.
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # 2) The user's taste profile.
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "target_valence": 0.9,
        "target_tempo_bpm": 120,
    }

    # 3) Show the profile.
    print("\nUser Profile:")
    print(f"Genre: {user_prefs['favorite_genre']}")
    print(f"Mood: {user_prefs['favorite_mood']}")
    print(f"Target Energy: {user_prefs['target_energy']}")
    print(f"Target Valence: {user_prefs['target_valence']}")
    print(f"Target Tempo: {user_prefs['target_tempo_bpm']} BPM")

    # 4) Get the top recommendations.
    recommendations = recommend_songs(user_prefs, songs, k=5)

    # 5) Print each recommendation with its score and reasons.
    print("\nTop Recommendations:\n")
    for position, rec in enumerate(recommendations, start=1):
        song = rec["song"]
        print(f"{position}. {song['title']}")
        print(f"Score: {rec['score']:.2f}")
        print("Reasons:")
        for reason in rec["reasons"]:
            print(f"- {reason}")
        print()


if __name__ == "__main__":
    main()
