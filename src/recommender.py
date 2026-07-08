from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

# ---------------------------------------------------------------------------
# Algorithm Recipe (weights)
# These say how much each feature is worth. Genre matters most, then mood,
# then the numeric "vibe" features. Change these to run experiments!
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
    """
    Loads songs from a CSV file into a list of dictionaries.
    Numeric columns are turned from text into numbers so we can do math on them.
    Required by src/main.py
    """
    numeric_columns = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            for column in numeric_columns:
                row[column] = float(row[column])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences (dictionary version).
    Uses the same Algorithm Recipe as the Recommender class above.
    Expected return format: (score, reasons)
    """
    # Read the user's preferences, using sensible defaults if a key is missing.
    fav_genre = user_prefs.get("genre")
    fav_mood = user_prefs.get("mood")
    target_energy = user_prefs.get("energy", 0.5)
    target_valence = user_prefs.get("valence", 0.5)
    target_tempo = user_prefs.get("tempo_bpm", 100.0)
    likes_acoustic = user_prefs.get("likes_acoustic", False)

    points = 0.0
    reasons: List[str] = []

    if song["genre"] == fav_genre:
        points += WEIGHT_GENRE
        reasons.append(f"matches your favorite genre ({song['genre']})")

    if song["mood"] == fav_mood:
        points += WEIGHT_MOOD
        reasons.append(f"matches your favorite mood ({song['mood']})")

    energy_closeness = 1 - abs(song["energy"] - target_energy)
    points += WEIGHT_ENERGY * energy_closeness
    if energy_closeness > 0.8:
        reasons.append("energy is close to what you like")

    valence_closeness = 1 - abs(song["valence"] - target_valence)
    points += WEIGHT_VALENCE * valence_closeness

    tempo_closeness = max(0.0, 1 - abs(song["tempo_bpm"] - target_tempo) / TEMPO_RANGE)
    points += WEIGHT_TEMPO * tempo_closeness

    if likes_acoustic and song["acousticness"] >= 0.5:
        points += WEIGHT_ACOUSTIC
        reasons.append("it is acoustic, which you like")

    return points, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Scores every song, ranks them best-to-worst, and returns the top k.
    Expected return format: (song_dict, score, explanation)
    """
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        points, reasons = score_song(user_prefs, song)
        if reasons:
            explanation = "it " + ", and ".join(reasons)
        else:
            explanation = "it is an okay general match"
        scored.append((song, points, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
