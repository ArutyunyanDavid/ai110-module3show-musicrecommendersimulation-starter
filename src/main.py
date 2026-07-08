"""
Command line runner for the Music Recommender Simulation.

This version shows off the optional challenge features:
- extra song features (danceability, acousticness, popularity, decade, etc.)
- multiple scoring modes (balanced / genre_first / mood_first / energy_focused)
- an optional diversity penalty
- a clean table-style output (built with plain Python, no extra libraries)

Run it from the project root with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# User profiles. These now include the new preference keys too.
# ---------------------------------------------------------------------------
high_energy_pop = {
    "name": "High-Energy Pop",
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.9,
    "target_valence": 0.9,
    "target_tempo_bpm": 125,
    "target_danceability": 0.85,
    "target_acousticness": 0.1,
    "target_popularity": 75,
    "preferred_decade": 2020,
    "preferred_detailed_mood": "hype",
}

chill_lofi = {
    "name": "Chill Lofi",
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.3,
    "target_valence": 0.55,
    "target_tempo_bpm": 78,
    "target_danceability": 0.55,
    "target_acousticness": 0.8,
    "target_popularity": 50,
    "preferred_decade": 2020,
    "preferred_detailed_mood": "focused",
}


def print_table(recommendations: list) -> None:
    """Print the recommendations as a simple text table, then the reasons."""
    headers = ["Rank", "Title", "Artist", "Genre", "Mood", "Score"]
    rows = []
    for rank, rec in enumerate(recommendations, start=1):
        song = rec["song"]
        rows.append([
            str(rank),
            song["title"],
            song["artist"],
            song["genre"],
            song["mood"],
            f"{rec['score']:.2f}",
        ])

    # Find the widest cell in each column so the columns line up.
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def format_row(cells: list) -> str:
        return " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells))

    # Header, a divider line, then every row.
    print(format_row(headers))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(format_row(row))

    # Reasons are usually too long for a table cell, so we list them below.
    print("\nReasons:")
    for rank, rec in enumerate(recommendations, start=1):
        print(f"{rank}. {rec['song']['title']}")
        if rec["reasons"]:
            for reason in rec["reasons"]:
                print(f"   - {reason}")
        else:
            print("   - (no strong matches)")


def run_demo(profile: dict, songs: list, mode: str, use_diversity: bool) -> None:
    """Run one recommendation demo and print it clearly."""
    print("=" * 60)
    print(f"Profile: {profile['name']}")
    print(f"Scoring Mode: {mode}")
    print(f"Diversity: {'on' if use_diversity else 'off'}")
    print()

    recommendations = recommend_songs(
        profile, songs, k=5, mode=mode, use_diversity=use_diversity
    )
    print_table(recommendations)
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # Demo 1: energy-focused mode for a high-energy listener.
    run_demo(high_energy_pop, songs, mode="energy_focused", use_diversity=False)

    # Demo 2 and 3: same profile and mode, WITHOUT then WITH diversity, so I can
    # see how the diversity penalty changes the list.
    run_demo(chill_lofi, songs, mode="genre_first", use_diversity=False)
    run_demo(chill_lofi, songs, mode="genre_first", use_diversity=True)


if __name__ == "__main__":
    main()
