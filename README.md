# 🎵 Music Recommender Simulation

## Project Summary

This project extends a simple content-based music recommender into a more structured applied AI system. The system ranks songs by matching them to a user’s stated preferences, and it now includes extra song attributes, a diversity penalty, a reliability guard, and a small evaluation harness.

---

## How The System Works

Real-world recommenders such as Spotify or YouTube use many signals at once, including genre, mood, tempo, listening history, and popularity. This project uses a smaller version of that idea. It takes a user profile with preferences such as favorite genre, favorite mood, target energy, and acoustic taste, then compares those preferences with each song’s features to produce a score.

The system uses input data (song features and user preferences), then ranks the songs by score and returns the best matches. The explanations are generated from the same scoring logic so the results are easier to understand.

### What each song stores
Each song includes:
- genre
- mood
- energy
- acousticness
- popularity
- release decade
- mood tags
- lyrical depth
- instrumentalness
- vocal energy

### What the user profile stores
Each profile includes:
- favorite genre
- favorite mood
- target energy
- acoustic preference
- optional advanced preferences such as popularity or release decade

### Algorithm Recipe
The recommender uses weighted scoring for genre, mood, energy, acousticness, popularity, release decade, mood tags, lyrical depth, instrumentalness, and vocal energy. It also applies a diversity penalty so the top results do not repeat the same artist or genre too often.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python3 -m src.main
```

4. Run the evaluation summary:

```bash
python3 evaluate_recommender.py
```

### Running Tests

Run the test suite with:

```bash
python3 -m pytest -q
```

---

## Sample Recommendation Output

Example output from running the app:

```text
=== High-Energy Pop ===
Rank Title                  Artist          Genre        Score   Reasons
1    Sunrise City           Neon Echo       pop            6.88 matches your favorite genre: pop; matches your favorite mood: happy; energy is very close to your target; stays relatively non-acoustic.
2    Rooftop Lights         Indigo Parade   indie pop      5.64 matches your favorite mood: happy; energy is very close to your target; stays relatively non-acoustic.
3    Gym Hero               Max Pulse       pop            5.28 matches your favorite genre: pop; energy is very close to your target; stays relatively non-acoustic.
```

Example evaluation summary:

```text
Evaluation Summary
==================
High-Energy Pop: Sunrise City, Rooftop Lights, Gym Hero
Chill Lofi: Library Rain, Midnight Coding, Spacewalk Thoughts
Deep Intense Rock: Storm Runner, Gym Hero, City Pulse
```

---

## Experiments and Findings

I tested three user profiles:
- High-Energy Pop
- Chill Lofi
- Deep Intense Rock

The results changed when the scoring weights shifted toward energy and the recommender applied the diversity penalty. This made the recommendations less repetitive and more balanced across artists and genres.

---

## Reliability and Guardrails

The recommender now validates user preferences before scoring. If a user provides an invalid energy value outside the range $0.0$ to $1.0$, the system raises a clear error instead of silently continuing.

---

## Reflection

See [model_card.md](model_card.md) for the completed model card and reflection.



