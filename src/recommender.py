from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

# ---------------------------------------------------------------------------
# Algorithm Recipe (weights)
# These weights are used by the Recommender CLASS below (the OOP version that
# the tests use). The functional version, score_song(), uses SCORING_MODES.
# ---------------------------------------------------------------------------
WEIGHT_GENRE = 2.0
WEIGHT_MOOD = 1.0
WEIGHT_ENERGY = 1.0
WEIGHT_VALENCE = 1.0
WEIGHT_TEMPO = 1.0
WEIGHT_ACOUSTIC = 1.0  # optional bonus, only used if the user sets likes_acoustic

# How many bpm apart counts as "totally different" tempo. Used to turn a big
# tempo number into a small 0-to-1 closeness score.
TEMPO_RANGE = 60.0

# ---------------------------------------------------------------------------
# Scoring modes (a simple "Strategy pattern").
# Each mode is just a dictionary of weights. score_song() looks up the mode and
# uses its weights, so we can rank songs in different ways WITHOUT writing a new
# scoring function for each one.
#   - balanced:       everything counts a normal amount (the default)
#   - genre_first:    genre is king; everything else matters less
#   - mood_first:     mood and detailed mood matter most
#   - energy_focused: energy, tempo, and danceability rule (gym / party music)
# ---------------------------------------------------------------------------
SCORING_MODES = {
    "balanced": {
        "genre": 2.0, "mood": 1.0, "detailed_mood": 1.0,
        "energy": 1.0, "valence": 1.0, "tempo": 1.0,
        "danceability": 1.0, "acousticness": 1.0,
        "popularity": 1.0, "decade": 1.0,
    },
    "genre_first": {
        "genre": 4.0, "mood": 1.0, "detailed_mood": 0.5,
        "energy": 0.5, "valence": 0.5, "tempo": 0.5,
        "danceability": 0.5, "acousticness": 0.5,
        "popularity": 0.5, "decade": 0.5,
    },
    "mood_first": {
        "genre": 1.0, "mood": 3.0, "detailed_mood": 3.0,
        "energy": 1.0, "valence": 1.0, "tempo": 0.5,
        "danceability": 0.5, "acousticness": 0.5,
        "popularity": 0.5, "decade": 0.5,
    },
    "energy_focused": {
        "genre": 1.0, "mood": 0.5, "detailed_mood": 0.5,
        "energy": 3.0, "valence": 0.5, "tempo": 2.0,
        "danceability": 2.0, "acousticness": 0.5,
        "popularity": 0.5, "decade": 0.5,
    },
}

# A closeness score must be at least this good before we list it as a "reason".
# This keeps the reason list short and only shows features that really matched.
REASON_THRESHOLD = 0.7

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    # New fields for the "full" recipe. They have defaults so older code that
    # only sets the first four fields still works.
    target_valence: float = 0.5
    target_tempo: float = 100.0

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """
        SCORING RULE: give ONE song a number of points based on how well it
        matches the user. Also collect reasons so we can explain the score.
        """
        points = 0.0
        reasons: List[str] = []

        # --- Category matches (yes/no) ---
        if song.genre == user.favorite_genre:
            points += WEIGHT_GENRE
            reasons.append(f"matches your favorite genre ({song.genre})")

        if song.mood == user.favorite_mood:
            points += WEIGHT_MOOD
            reasons.append(f"matches your favorite mood ({song.mood})")

        # --- Numeric "closer is better" scores ---
        # energy and valence are already 0-1, so the gap is at most 1.
        energy_closeness = 1 - abs(song.energy - user.target_energy)
        points += WEIGHT_ENERGY * energy_closeness
        if energy_closeness > 0.8:
            reasons.append("energy is close to what you like")

        valence_closeness = 1 - abs(song.valence - user.target_valence)
        points += WEIGHT_VALENCE * valence_closeness
        if valence_closeness > 0.8:
            reasons.append("the happy/sad vibe fits you")

        # tempo is a big number, so divide by a range and don't go below 0.
        tempo_closeness = max(0.0, 1 - abs(song.tempo_bpm - user.target_tempo) / TEMPO_RANGE)
        points += WEIGHT_TEMPO * tempo_closeness
        if tempo_closeness > 0.8:
            reasons.append("the tempo is close to what you like")

        # --- Acoustic preference ---
        if user.likes_acoustic and song.acousticness >= 0.5:
            points += WEIGHT_ACOUSTIC
            reasons.append("it is acoustic, which you like")

        return points, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        RANKING RULE: score every song, sort from best to worst, keep top k.
        """
        scored = [(song, self.score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _points in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Turn the reasons list into a friendly sentence."""
        points, reasons = self.score(user, song)
        if reasons:
            return f"Score {points:.2f} because it " + ", and ".join(reasons) + "."
        return f"Score {points:.2f}. It does not match your preferences very well."

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and convert numeric fields into numbers."""
    # Columns that should become decimal numbers.
    float_columns = {
        "energy", "tempo_bpm", "valence", "danceability",
        "acousticness", "instrumentalness", "popularity",
    }
    # Columns that should become whole numbers.
    int_columns = {"id", "release_decade"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only convert a column if it actually exists and is not blank, so
            # this stays safe even if the CSV is missing one of these columns.
            for column in int_columns:
                if row.get(column):
                    row[column] = int(row[column])
            for column in float_columns:
                if row.get(column):
                    row[column] = float(row[column])
            songs.append(row)
    return songs

def _closeness_0_1(song_value: float, target_value: float) -> float:
    """Closeness for 0-to-1 features: 1.0 means identical, 0.0 means opposite."""
    return 1 - abs(song_value - target_value)


def _closeness_range(song_value: float, target_value: float, span: float) -> float:
    """Closeness for big numbers (like tempo): divide the gap by a span."""
    return max(0.0, 1 - abs(song_value - target_value) / span)


def _popularity_closeness(song_pop: float, target_pop: float) -> float:
    """Full credit if the song is at least as popular as wanted, else partial."""
    if song_pop >= target_pop:
        return 1.0
    return max(0.0, 1 - (target_pop - song_pop) / 100.0)


def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, List[str]]:
    """Score one song using the chosen scoring mode; return (score, reasons)."""
    # Pick the weight dictionary for this mode (fall back to balanced).
    weights = SCORING_MODES.get(mode, SCORING_MODES["balanced"])

    score = 0.0
    reasons: List[str] = []

    # --- Word matches: all-or-nothing points ---
    if user_prefs.get("favorite_genre") == song.get("genre"):
        score += weights["genre"]
        reasons.append(f"genre match (+{weights['genre']:.1f})")

    if user_prefs.get("favorite_mood") == song.get("mood"):
        score += weights["mood"]
        reasons.append(f"mood match (+{weights['mood']:.1f})")

    if "preferred_detailed_mood" in user_prefs and \
            user_prefs["preferred_detailed_mood"] == song.get("detailed_mood"):
        score += weights["detailed_mood"]
        reasons.append(f"detailed mood match (+{weights['detailed_mood']:.1f})")

    if "preferred_decade" in user_prefs and \
            user_prefs["preferred_decade"] == song.get("release_decade"):
        score += weights["decade"]
        reasons.append(f"decade match (+{weights['decade']:.1f})")

    # --- Number features: closer to the target = more points ---
    # Each block only runs if the user gave a target (and the song has the value),
    # so it is safe even if a column or preference is missing.
    if "target_energy" in user_prefs:
        close = _closeness_0_1(song["energy"], user_prefs["target_energy"])
        pts = weights["energy"] * close
        score += pts
        if close >= REASON_THRESHOLD:
            reasons.append(f"energy close to target (+{pts:.2f})")

    if "target_valence" in user_prefs:
        close = _closeness_0_1(song["valence"], user_prefs["target_valence"])
        pts = weights["valence"] * close
        score += pts
        if close >= REASON_THRESHOLD:
            reasons.append(f"valence close to target (+{pts:.2f})")

    if "target_tempo_bpm" in user_prefs:
        close = _closeness_range(song["tempo_bpm"], user_prefs["target_tempo_bpm"], TEMPO_RANGE)
        pts = weights["tempo"] * close
        score += pts
        if close >= REASON_THRESHOLD:
            reasons.append(f"tempo close to target (+{pts:.2f})")

    if "target_danceability" in user_prefs and "danceability" in song:
        close = _closeness_0_1(song["danceability"], user_prefs["target_danceability"])
        pts = weights["danceability"] * close
        score += pts
        if close >= REASON_THRESHOLD:
            reasons.append(f"danceability close to target (+{pts:.2f})")

    if "target_acousticness" in user_prefs and "acousticness" in song:
        close = _closeness_0_1(song["acousticness"], user_prefs["target_acousticness"])
        pts = weights["acousticness"] * close
        score += pts
        if close >= REASON_THRESHOLD:
            reasons.append(f"acousticness close to target (+{pts:.2f})")

    if "target_popularity" in user_prefs and "popularity" in song:
        close = _popularity_closeness(song["popularity"], user_prefs["target_popularity"])
        pts = weights["popularity"] * close
        score += pts
        if close >= REASON_THRESHOLD:
            reasons.append(f"popular enough (+{pts:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    mode: str = "balanced", use_diversity: bool = False) -> List[Dict]:
    """Score all songs, rank them, and return the top k (optionally diverse)."""
    # Step 1: give every song a base score using the chosen mode.
    scored: List[Dict] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode)
        scored.append({"song": song, "score": score, "reasons": list(reasons)})

    # Simple ranking: just sort by score, highest first.
    if not use_diversity:
        ranked = sorted(scored, key=lambda item: item["score"], reverse=True)
        return ranked[:k]

    # Step 2 (diversity ON): pick songs one at a time. Each time we pick one, we
    # lower the score of any leftover song that repeats an artist or genre we
    # already chose. This happens during RANKING, not inside score_song, because
    # one song's base score should not depend on which OTHER songs got picked --
    # that is a property of the whole list, so it belongs here.
    remaining = list(scored)
    selected: List[Dict] = []
    while remaining and len(selected) < k:
        chosen_artists = [item["song"]["artist"] for item in selected]
        chosen_genres = [item["song"]["genre"] for item in selected]

        best_item = None
        best_adjusted = None
        best_penalty_reasons: List[str] = []

        for item in remaining:
            penalty = 0.0
            penalty_reasons: List[str] = []
            artist = item["song"]["artist"]
            genre = item["song"]["genre"]

            if artist in chosen_artists:
                penalty += 1.0
                penalty_reasons.append("diversity penalty: same artist already recommended (-1.0)")
            if chosen_genres.count(genre) >= 2:
                penalty += 0.5
                penalty_reasons.append("diversity penalty: genre already shown often (-0.5)")

            adjusted = item["score"] - penalty
            if best_adjusted is None or adjusted > best_adjusted:
                best_item = item
                best_adjusted = adjusted
                best_penalty_reasons = penalty_reasons

        # Lock in the winner with its adjusted score and any penalty reasons.
        best_item["score"] = best_adjusted
        best_item["reasons"] = best_item["reasons"] + best_penalty_reasons
        selected.append(best_item)
        remaining.remove(best_item)

    return selected
