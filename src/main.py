"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import DEFAULT_TASTE_PROFILE, load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_prefs = {
        "genre": DEFAULT_TASTE_PROFILE["favorite_genre"],
        "mood": DEFAULT_TASTE_PROFILE["favorite_mood"],
        "energy": DEFAULT_TASTE_PROFILE["target_energy"],
        "likes_acoustic": DEFAULT_TASTE_PROFILE["likes_acoustic"],
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
