# 🎵 Music Recommender Simulation

## Project Summary

This project builds a simple content-based music recommender that ranks songs by how well they match a user’s stated taste. The system uses a lightweight scoring recipe based on genre, mood, and energy so the recommendations are easy to explain and easy to adjust.

---

## How The System Works

This project builds a simple content-based music recommender. It looks at a song’s musical features and compares them to a user’s taste profile to decide which songs are the best match.

### What each song stores
Each `Song` includes:
- `genre`: the style of the song
- `mood`: the emotional tone
- `energy`: how intense or active the song feels
- `tempo_bpm`: how fast the song is
- `valence`: how positive or uplifting the song sounds
- `danceability`: how easy it is to dance to
- `acousticness`: how acoustic or natural the sound feels

### What the user profile stores
Each `UserProfile` stores the user’s preferences, including:
- favorite genre
- favorite mood
- preferred energy level
- whether they prefer acoustic songs

### Algorithm Recipe
The recommender uses the following scoring recipe:
- +2.0 points for a genre match
- +1.0 point for a mood match
- similarity points based on how close the song’s energy is to the user’s target energy
- a small bonus for acoustic preference, so the system can still favor songs that match the user’s taste beyond genre and mood

In practice, this means a song that matches both the preferred genre and the preferred mood will score strongly, while songs that are only close in energy will still be considered but rank lower. The final recommendation list is created by sorting all scored songs from highest to lowest score and returning the top results.

### Expected Biases
This system may over-prioritize genre, which could cause it to miss strong songs that match the user’s mood or energy better but fall in a different genre. It also relies on a small set of handcrafted features, so it may not capture deeper musical preferences that a user would actually care about.

A simple flow looks like this:

User profile -> compare with song features -> calculate score -> rank songs -> recommend top matches

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the default profile (genre=pop, mood=happy, energy=0.8, likes_acoustic=False):

```
Loading songs from data/songs.csv...
Loaded songs: 18

Top recommendations:

Sunrise City - Score: 5.96
Because: matches your favorite genre: pop; matches your favorite mood: happy; energy is very close to your target; stays relatively non-acoustic.

Gym Hero - Score: 4.74
Because: matches your favorite genre: pop; energy is very close to your target; stays relatively non-acoustic.

Rooftop Lights - Score: 3.92
Because: matches your favorite mood: happy; energy is very close to your target; stays relatively non-acoustic.

Night Drive Loop - Score: 2.90
Because: energy is very close to your target; stays relatively non-acoustic.

Neon Skyline - Score: 2.88
Because: energy is very close to your target; stays relatively non-acoustic.
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



