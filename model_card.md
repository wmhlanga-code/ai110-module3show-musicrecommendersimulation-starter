# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

---

## 2. Goal / Task

This recommender tries to suggest songs that fit a user’s taste. It predicts which songs a person would likely enjoy based on a small set of preferences.

---

## 3. Data Used

The model uses a catalog of 18 songs. Each song has features such as genre, mood, energy, and acousticness. The dataset is small, so it cannot capture the full range of real music taste.

---

## 4. Algorithm Summary

The system gives points to songs that match a user’s favorite genre, mood, and energy level. It also checks whether the song fits the user’s acoustic preference. Songs with the highest total score are shown first.

---

## 5. Observed Behavior / Biases

The system can feel too rigid because it relies on exact matches for genre and mood. It may also overvalue a few obvious songs when the catalog is small, which can create a narrow or repetitive set of recommendations.

---

## 6. Evaluation Process

I tested several user profiles, including a high-energy pop profile, a chill lofi profile, and a deep intense rock profile. I compared the top recommendations and checked whether they matched my intuition. I also ran a small experiment by making energy matter more and genre matter less to see how the rankings changed.

---

## 7. Intended Use and Non-Intended Use

This model is intended for learning, classroom exploration, and simple demo-style recommendation. It should not be used as a real-world music recommendation system for actual users, because it does not use listening history, lyrics, or deeper musical context.

---

## 8. Ideas for Improvement

I would like to add more song features, such as tempo or valence. I would also like to use a larger dataset so the recommendations feel more diverse. Another improvement would be to make the scoring less strict so similar moods and genres can still be recommended.

---

## 9. Personal Reflection

My biggest learning moment was realizing how small changes in the scoring rules can change the whole list of recommendations. Using AI tools helped me move faster, especially when I needed help explaining why a song ranked high or when I wanted to test a new idea quickly. I was surprised that a simple algorithm could still feel convincing, even though it only used a few basic features. If I extended this project, I would try a larger dataset and more advanced features so the recommendations could feel more realistic.

