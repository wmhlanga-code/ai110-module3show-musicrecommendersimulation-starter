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
    popularity: float = 0.0
    release_decade: int = 0
    mood_tags: str = ""
    lyrical_depth: float = 0.0
    instrumentalness: float = 0.0
    vocal_energy: float = 0.0


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
    preferred_popularity: float = 0.0
    preferred_release_decade: Optional[int] = None
    preferred_mood_tags: Optional[List[str]] = None
    preferred_lyrical_depth: float = 0.0
    preferred_instrumentalness: float = 0.0
    preferred_vocal_energy: float = 0.0


DEFAULT_TASTE_PROFILE = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.8,
    "likes_acoustic": False,
}

# Experimental weights used for the small data experiment.
# The energy weight was increased while the genre weight was reduced.
GENRE_WEIGHT = 1.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 4.0
ACOUSTIC_WEIGHT = 1.0
POPULARITY_WEIGHT = 0.6
RELEASE_DECADE_WEIGHT = 0.4
MOOD_TAG_WEIGHT = 0.5
LYRICAL_DEPTH_WEIGHT = 0.3
INSTRUMENTALNESS_WEIGHT = 0.3
VOCAL_ENERGY_WEIGHT = 0.3
DIVERSITY_PENALTY_ARTIST = 0.8
DIVERSITY_PENALTY_GENRE = 0.4


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

            score, _ = score_song(prefs, song)
            scored_songs.append((score, song))

        scored_songs.sort(key=lambda item: item[0], reverse=True)
        selected_songs = _select_diverse_recommendations(scored_songs, k)
        return [song for _, song in selected_songs]

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
                    "popularity": float(row.get("popularity", 0.0)),
                    "release_decade": int(row.get("release_decade", 0)),
                    "mood_tags": row.get("mood_tags", ""),
                    "lyrical_depth": float(row.get("lyrical_depth", 0.0)),
                    "instrumentalness": float(row.get("instrumentalness", 0.0)),
                    "vocal_energy": float(row.get("vocal_energy", 0.0)),
                }
            )
    return songs


def _get_song_value(song: object, key: str, default: object = None) -> object:
    if isinstance(song, dict):
        return song.get(key, default)
    return getattr(song, key, default)


def validate_user_preferences(user_prefs: object) -> Dict[str, object]:
    """Validate user preferences and return normalized preferences."""
    prefs = _coerce_user_preferences(user_prefs)
    energy = float(prefs.get("energy", 0.0))
    if not 0.0 <= energy <= 1.0:
        raise ValueError("target_energy must be between 0.0 and 1.0")
    return prefs


def _coerce_user_preferences(user_prefs: object) -> Dict[str, object]:
    if isinstance(user_prefs, UserProfile):
        return {
            "genre": user_prefs.favorite_genre.lower(),
            "mood": user_prefs.favorite_mood.lower(),
            "energy": user_prefs.target_energy,
            "likes_acoustic": user_prefs.likes_acoustic,
            "preferred_popularity": getattr(user_prefs, "preferred_popularity", 0.0),
            "preferred_release_decade": getattr(user_prefs, "preferred_release_decade", None),
            "preferred_mood_tags": getattr(user_prefs, "preferred_mood_tags", []),
            "preferred_lyrical_depth": getattr(user_prefs, "preferred_lyrical_depth", 0.0),
            "preferred_instrumentalness": getattr(user_prefs, "preferred_instrumentalness", 0.0),
            "preferred_vocal_energy": getattr(user_prefs, "preferred_vocal_energy", 0.0),
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
            "preferred_popularity": float(user_prefs.get("preferred_popularity", 0.0)),
            "preferred_release_decade": user_prefs.get("preferred_release_decade"),
            "preferred_mood_tags": [
                tag.strip().lower()
                for tag in str(user_prefs.get("preferred_mood_tags", "")).split(",")
                if tag.strip()
            ],
            "preferred_lyrical_depth": float(user_prefs.get("preferred_lyrical_depth", 0.0)),
            "preferred_instrumentalness": float(user_prefs.get("preferred_instrumentalness", 0.0)),
            "preferred_vocal_energy": float(user_prefs.get("preferred_vocal_energy", 0.0)),
        }

    return {
        "genre": "",
        "mood": "",
        "energy": 0.0,
        "likes_acoustic": False,
        "preferred_popularity": 0.0,
        "preferred_release_decade": None,
        "preferred_mood_tags": [],
        "preferred_lyrical_depth": 0.0,
        "preferred_instrumentalness": 0.0,
        "preferred_vocal_energy": 0.0,
    }


def score_song(user_prefs: object, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences, returning (score, list of human-readable reasons)."""
    prefs = validate_user_preferences(user_prefs)
    song_genre = str(_get_song_value(song, "genre", "")).strip().lower()
    song_mood = str(_get_song_value(song, "mood", "")).strip().lower()
    song_energy = float(_get_song_value(song, "energy", 0.0))
    song_acousticness = float(_get_song_value(song, "acousticness", 0.0))
    song_popularity = float(_get_song_value(song, "popularity", 0.0))
    song_release_decade = int(_get_song_value(song, "release_decade", 0))
    song_mood_tags = [tag.strip().lower() for tag in str(_get_song_value(song, "mood_tags", "")).split(",") if tag.strip()]
    song_lyrical_depth = float(_get_song_value(song, "lyrical_depth", 0.0))
    song_instrumentalness = float(_get_song_value(song, "instrumentalness", 0.0))
    song_vocal_energy = float(_get_song_value(song, "vocal_energy", 0.0))

    score = 0.0
    reasons: List[str] = []

    if prefs["genre"] and song_genre == str(prefs["genre"]):
        score += GENRE_WEIGHT
        reasons.append(f"matches your favorite genre: {song_genre}")

    if prefs["mood"] and song_mood == str(prefs["mood"]):
        score += MOOD_WEIGHT
        reasons.append(f"matches your favorite mood: {song_mood}")

    energy_gap = abs(song_energy - float(prefs["energy"]))
    energy_score = max(0.0, 1.0 - energy_gap)
    score += energy_score * ENERGY_WEIGHT
    if energy_gap <= 0.15:
        reasons.append("energy is very close to your target")
    else:
        reasons.append("energy is less aligned with your target")

    if bool(prefs["likes_acoustic"]):
        if song_acousticness >= 0.5:
            score += ACOUSTIC_WEIGHT
            reasons.append("is acoustic, which you prefer")
        else:
            reasons.append("is less acoustic than you prefer")
    else:
        if song_acousticness < 0.5:
            score += ACOUSTIC_WEIGHT
            reasons.append("stays relatively non-acoustic")
        else:
            reasons.append("leans acoustic, which you do not prefer")

    popularity_gap = abs(song_popularity - float(prefs.get("preferred_popularity", 0.0)))
    popularity_score = max(0.0, 1.0 - (popularity_gap / 100.0))
    if float(prefs.get("preferred_popularity", 0.0)) > 0:
        score += popularity_score * POPULARITY_WEIGHT
        reasons.append("has popularity close to your target")

    if prefs.get("preferred_release_decade") is not None and prefs.get("preferred_release_decade"):
        release_gap = abs(song_release_decade - int(prefs.get("preferred_release_decade")))
        release_score = max(0.0, 1.0 - (release_gap / 10.0))
        score += release_score * RELEASE_DECADE_WEIGHT
        reasons.append("has a release decade close to your target")

    preferred_mood_tags = set(prefs.get("preferred_mood_tags", []))
    if preferred_mood_tags:
        overlap = len(preferred_mood_tags.intersection(set(song_mood_tags)))
        if overlap:
            score += overlap * MOOD_TAG_WEIGHT
            reasons.append("shares mood tags you like")

    lyrical_depth_gap = abs(song_lyrical_depth - float(prefs.get("preferred_lyrical_depth", 0.0)))
    lyrical_depth_score = max(0.0, 1.0 - lyrical_depth_gap)
    if float(prefs.get("preferred_lyrical_depth", 0.0)) > 0:
        score += lyrical_depth_score * LYRICAL_DEPTH_WEIGHT
        reasons.append("has lyrical depth close to your target")

    instrumentalness_gap = abs(song_instrumentalness - float(prefs.get("preferred_instrumentalness", 0.0)))
    instrumentalness_score = max(0.0, 1.0 - instrumentalness_gap)
    if float(prefs.get("preferred_instrumentalness", 0.0)) > 0:
        score += instrumentalness_score * INSTRUMENTALNESS_WEIGHT
        reasons.append("has instrumentalness close to your target")

    vocal_energy_gap = abs(song_vocal_energy - float(prefs.get("preferred_vocal_energy", 0.0)))
    vocal_energy_score = max(0.0, 1.0 - vocal_energy_gap)
    if float(prefs.get("preferred_vocal_energy", 0.0)) > 0:
        score += vocal_energy_score * VOCAL_ENERGY_WEIGHT
        reasons.append("has vocal energy close to your target")

    return round(score, 3), reasons


def _select_diverse_recommendations(scored_songs: List[Tuple[float, object]], k: int) -> List[Tuple[float, object]]:
    """Greedily select recommendations that are both high-scoring and diverse."""
    remaining = [
        {
            "score": score,
            "item": item,
        }
        for score, item in scored_songs
    ]
    selected: List[Tuple[float, object]] = []
    seen_artists = set()
    seen_genres = set()

    for _ in range(min(k, len(remaining))):
        best_index = None
        best_candidate = None
        best_adjusted_score = None

        for index, entry in enumerate(remaining):
            item = entry["item"]
            song = item[0] if isinstance(item, tuple) else item
            artist = song.get("artist") if isinstance(song, dict) else getattr(song, "artist", "")
            genre = song.get("genre") if isinstance(song, dict) else getattr(song, "genre", "")

            penalty = 0.0
            if artist in seen_artists:
                penalty += DIVERSITY_PENALTY_ARTIST
            if genre in seen_genres:
                penalty += DIVERSITY_PENALTY_GENRE

            adjusted_score = entry["score"] - penalty
            if best_adjusted_score is None or adjusted_score > best_adjusted_score:
                best_index = index
                best_candidate = entry
                best_adjusted_score = adjusted_score

        if best_candidate is None:
            break

        selected.append((best_adjusted_score, best_candidate["item"]))
        remaining.pop(best_index)

        item = best_candidate["item"]
        song = item[0] if isinstance(item, tuple) else item
        artist = song.get("artist") if isinstance(song, dict) else getattr(song, "artist", "")
        genre = song.get("genre") if isinstance(song, dict) else getattr(song, "genre", "")
        seen_artists.add(artist)
        seen_genres.add(genre)

    return selected


def recommend_songs(user_prefs: object, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank every song with score_song and return the top k as (song, score, explanation) tuples."""
    validated_prefs = validate_user_preferences(user_prefs)
    scored_songs = []
    for song in songs:
        score, reasons = score_song(validated_prefs, song)
        explanation = "; ".join(reasons) + "."
        scored_songs.append((score, (song, score, explanation)))

    selected = _select_diverse_recommendations(scored_songs, k)
    return [
        (song, adjusted_score, explanation)
        for adjusted_score, (song, _, explanation) in selected
    ]
