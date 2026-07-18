"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import DEFAULT_TASTE_PROFILE, load_songs, recommend_songs


def print_recommendation_table(profile_name: str, recommendations: list) -> None:
    print(f"\n=== {profile_name} ===")
    print(f"{'Rank':<4} {'Title':<22} {'Artist':<15} {'Genre':<12} {'Score':<7} {'Reasons'}")
    print("-" * 110)

    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reason_text = explanation[:90] + ("..." if len(explanation) > 90 else "")
        print(f"{index:<4} {song['title']:<22} {song['artist']:<15} {song['genre']:<12} {score:>6.2f} {reason_text}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_profiles = [
        {
            "name": "High-Energy Pop",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.85,
            "likes_acoustic": False,
        },
        {
            "name": "Chill Lofi",
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "likes_acoustic": True,
        },
        {
            "name": "Deep Intense Rock",
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9,
            "likes_acoustic": False,
        },
    ]

    for profile in user_profiles:
        recommendations = recommend_songs(profile, songs, k=5)
        print_recommendation_table(profile["name"], recommendations)


if __name__ == "__main__":
    main()
