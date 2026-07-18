from pathlib import Path
from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    profiles = [
        {"name": "High-Energy Pop", "genre": "pop", "mood": "happy", "energy": 0.85, "likes_acoustic": False},
        {"name": "Chill Lofi", "genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
        {"name": "Deep Intense Rock", "genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
    ]

    print("Evaluation Summary")
    print("==================")
    for profile in profiles:
        recommendations = recommend_songs(profile, songs, k=3)
        top_titles = [song["title"] for song, _, _ in recommendations]
        print(f"{profile['name']}: {', '.join(top_titles)}")


if __name__ == "__main__":
    main()
