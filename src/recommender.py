import csv
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


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


DEFAULT_TASTE_PROFILE = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.8,
    "likes_acoustic": False,
}


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: object, k: int = 5) -> List[Song]:
        scored_songs = []
        for song in self.songs:
            if isinstance(user, UserProfile):
                prefs = {
                    "genre": user.favorite_genre,
                    "mood": user.favorite_mood,
                    "energy": user.target_energy,
                    "likes_acoustic": user.likes_acoustic,
                }
            elif isinstance(user, dict):
                prefs = {
                    "genre": user.get("favorite_genre") or user.get("genre"),
                    "mood": user.get("favorite_mood") or user.get("mood"),
                    "energy": user.get("target_energy", user.get("energy", 0.0)),
                    "likes_acoustic": user.get("likes_acoustic", False),
                }
            else:
                prefs = {"genre": "", "mood": "", "energy": 0.0, "likes_acoustic": False}

            score, _ = score_song(
                prefs,
                {
                    "genre": song.genre,
                    "mood": song.mood,
                    "energy": song.energy,
                    "acousticness": song.acousticness,
                },
            )
            scored_songs.append((score, song))

        scored_songs.sort(key=lambda item: item[0], reverse=True)
        return [song for _, song in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if user.favorite_genre.lower() == song.genre.lower():
            reasons.append(f"matches your favorite genre, {user.favorite_genre}")
        if user.favorite_mood.lower() == song.mood.lower():
            reasons.append(f"matches your favorite mood, {user.favorite_mood}")
        if abs(song.energy - user.target_energy) <= 0.15:
            reasons.append("has energy close to your target")
        elif song.energy > user.target_energy:
            reasons.append("is more energetic than your target")
        else:
            reasons.append("is less energetic than your target")
        if user.likes_acoustic and song.acousticness >= 0.5:
            reasons.append("leans acoustic, which you enjoy")
        elif not user.likes_acoustic and song.acousticness < 0.5:
            reasons.append("stays relatively non-acoustic, which fits your preference")

        if not reasons:
            return "It is a broadly compatible track."
        return "; ".join(reasons) + "."


def load_songs(csv_path: str) -> List[Dict]:
    """Read the song catalog from a CSV file into a list of dicts with numeric fields converted to float/int."""
    print(f"Loading songs from {csv_path}...")
    with open(csv_path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        songs = []
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs


def _coerce_user_preferences(user_prefs: object) -> Dict[str, object]:
    if isinstance(user_prefs, UserProfile):
        return {
            "genre": user_prefs.favorite_genre.lower(),
            "mood": user_prefs.favorite_mood.lower(),
            "energy": user_prefs.target_energy,
            "likes_acoustic": user_prefs.likes_acoustic,
        }

    if isinstance(user_prefs, dict):
        return {
            "genre": str(
                user_prefs.get("genre")
                or user_prefs.get("favorite_genre")
                or ""
            ).strip().lower(),
            "mood": str(
                user_prefs.get("mood")
                or user_prefs.get("favorite_mood")
                or ""
            ).strip().lower(),
            "energy": float(
                user_prefs.get("target_energy", user_prefs.get("energy", 0.0))
            ),
            "likes_acoustic": bool(user_prefs.get("likes_acoustic", False)),
        }

    return {"genre": "", "mood": "", "energy": 0.0, "likes_acoustic": False}


def score_song(user_prefs: object, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences, returning (score, list of human-readable reasons)."""
    prefs = _coerce_user_preferences(user_prefs)
    song_genre = str(song.get("genre", "")).strip().lower()
    song_mood = str(song.get("mood", "")).strip().lower()
    song_energy = float(song.get("energy", 0.0))
    song_acousticness = float(song.get("acousticness", 0.0))

    score = 0.0
    reasons: List[str] = []

    if prefs["genre"] and song_genre == str(prefs["genre"]):
        score += 2.0
        reasons.append(f"matches your favorite genre: {song_genre}")

    if prefs["mood"] and song_mood == str(prefs["mood"]):
        score += 1.0
        reasons.append(f"matches your favorite mood: {song_mood}")

    energy_gap = abs(song_energy - float(prefs["energy"]))
    energy_score = max(0.0, 1.0 - energy_gap)
    score += energy_score * 2.0
    if energy_gap <= 0.15:
        reasons.append("energy is very close to your target")
    else:
        reasons.append("energy is less aligned with your target")

    if bool(prefs["likes_acoustic"]):
        if song_acousticness >= 0.5:
            score += 1.0
            reasons.append("is acoustic, which you prefer")
        else:
            reasons.append("is less acoustic than you prefer")
    else:
        if song_acousticness < 0.5:
            score += 1.0
            reasons.append("stays relatively non-acoustic")
        else:
            reasons.append("leans acoustic, which you do not prefer")

    return round(score, 3), reasons


def recommend_songs(user_prefs: object, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank every song with score_song and return the top k as (song, score, explanation) tuples."""
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) + "."
        scored_songs.append((song, score, explanation))

    scored_songs.sort(key=lambda item: item[1], reverse=True)
    return scored_songs[:k]
