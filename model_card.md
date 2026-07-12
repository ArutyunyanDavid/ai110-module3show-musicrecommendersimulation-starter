# 🎧 Model Card: Music Recommender Simulation

## Model Name

**VibeFinder 1.0**

---

## Goal / Task

This recommender suggests songs that match a user's music taste profile. It looks
at each song in the CSV file and compares it to the user's favorite genre, favorite
mood, and target energy, valence, and tempo. The goal is to rank the songs from best
match to weakest match and show the top few.

---

## Data Used

- The data comes from `data/songs.csv`.
- It is a small dataset with 18 songs.
- Each song has features like title, artist, genre, mood, energy, valence, and tempo_bpm (plus danceability and acousticness).
- Some features are words, like genre and mood.
- Some features are numbers, like energy, valence, and tempo.

This is enough for a simple class project, but it is not enough for a real music app.
The dataset is small, and it does not include any real user actions like likes, skips,
saves, or playlists.

---

## Algorithm Summary

The recommender gives every song a score. A song gets +2.0 points if its genre matches
the user's favorite genre, and +1.0 point if its mood matches the user's favorite mood.
For energy, valence, and tempo, the system gives more points when the song is close to
the user's target values, and fewer points when it is far away. So a song with energy
0.75 scores higher than a song with energy 0.3 when the user wants 0.8.

After every song is scored, the program sorts the songs from highest score to lowest
score and shows the top recommendations. It also prints a list of reasons for each song
(like "genre match (+2.0)" or "energy close to target (+0.92)") so the user can see why
each song was picked.

---

## Observed Behavior / Biases

- The system can over-prioritize genre. A genre match gives a big +2.0 boost, so a song can win even if another song has a closer mood or energy match.
- The same song can show up for many profiles. "Gym Hero" appeared in the top 5 for four of my five profiles because it is pop with very high energy.
- The dataset is small, so there is not much variety. My "Chill Lofi" profile could only get the 3 lofi songs that exist.
- Some genres and moods are missing or rare. There is only one classical song, and there is no "sad" song at all, so the system does badly for those tastes.
- It can create a small filter bubble, because it mostly recommends songs that are already very similar to what the user said they like.

---

## Evaluation Process

I tested the recommender with 5 different user profiles: **High-Energy Pop**,
**Chill Lofi**, and **Deep Intense Rock** (normal tastes), plus two edge cases,
**Sad But High Energy** and **Genre Mismatch Test**. For each profile I looked at
the top 5 recommendations and checked if they made sense.

I also ran one experiment (Option A: Weight Shift). I changed genre from +2.0 down to
+1.0 and energy from up to +1.0 up to +2.0. The #1 song for each profile stayed the
same, but the lower ranks started favoring high-energy songs from other genres. For
example, a rock song jumped into the "High-Energy Pop" top 5, and the one classical
song fell out of the "Genre Mismatch Test" top 5. This showed me that small changes
in the weights can change the rankings, and that energy became stronger while genre
became weaker. I then set the weights back to the baseline.

Here are the real terminal outputs from the evaluation phase (the `balanced` /
baseline weights). Note: I later added a table format and scoring modes as optional
features, so the current `python -m src.main` prints these same scores in a table using
different demo modes. The scores below are the balanced-mode results I evaluated.

### High-Energy Pop Output

```text
Profile: High-Energy Pop
Preferences:
Genre: pop
Mood: happy
Target Energy: 0.9
Target Valence: 0.9
Target Tempo: 125 BPM

Top 5 Recommendations:

1. Sunrise City
Score: 5.74
Reasons:
- genre match (+2.0)
- mood match (+1.0)
- energy close to target (+0.92)
- valence close to target (+0.94)
- tempo close to target (+0.88)

2. Gym Hero
Score: 4.72
Reasons:
- genre match (+2.0)
- energy close to target (+0.97)
- valence close to target (+0.87)
- tempo close to target (+0.88)

3. Rooftop Lights
Score: 3.75
Reasons:
- mood match (+1.0)
- energy close to target (+0.86)
- valence close to target (+0.91)
- tempo close to target (+0.98)

4. Neon Horizon
Score: 2.75
Reasons:
- energy close to target (+0.95)
- valence close to target (+0.85)
- tempo close to target (+0.95)

5. City Lights Flow
Score: 2.20
Reasons:
- energy close to target (+0.90)
- valence close to target (+0.80)
- tempo close to target (+0.50)
```

### Chill Lofi Output

```text
Profile: Chill Lofi
Preferences:
Genre: lofi
Mood: calm
Target Energy: 0.3
Target Valence: 0.5
Target Tempo: 80 BPM

Top 5 Recommendations:

1. Focus Flow
Score: 4.81
Reasons:
- genre match (+2.0)
- energy close to target (+0.90)
- valence close to target (+0.91)
- tempo close to target (+1.00)

2. Midnight Coding
Score: 4.79
Reasons:
- genre match (+2.0)
- energy close to target (+0.88)
- valence close to target (+0.94)
- tempo close to target (+0.97)

3. Library Rain
Score: 4.72
Reasons:
- genre match (+2.0)
- energy close to target (+0.95)
- valence close to target (+0.90)
- tempo close to target (+0.87)

4. Old Porch Song
Score: 2.88
Reasons:
- energy close to target (+1.00)
- valence close to target (+0.95)
- tempo close to target (+0.93)

5. Coffee Shop Stories
Score: 2.55
Reasons:
- energy close to target (+0.93)
- valence close to target (+0.79)
- tempo close to target (+0.83)
```

### Deep Intense Rock Output

```text
Profile: Deep Intense Rock
Preferences:
Genre: rock
Mood: intense
Target Energy: 0.9
Target Valence: 0.4
Target Tempo: 140 BPM

Top 5 Recommendations:

1. Storm Runner
Score: 5.71
Reasons:
- genre match (+2.0)
- mood match (+1.0)
- energy close to target (+0.99)
- valence close to target (+0.92)
- tempo close to target (+0.80)

2. Gym Hero
Score: 3.47
Reasons:
- mood match (+1.0)
- energy close to target (+0.97)
- valence close to target (+0.63)
- tempo close to target (+0.87)

3. Iron Verdict
Score: 2.40
Reasons:
- energy close to target (+0.92)
- valence close to target (+0.95)
- tempo close to target (+0.53)

4. Neon Horizon
Score: 2.40
Reasons:
- energy close to target (+0.95)
- valence close to target (+0.65)
- tempo close to target (+0.80)

5. Night Drive Loop
Score: 2.26
Reasons:
- energy close to target (+0.85)
- valence close to target (+0.91)
- tempo close to target (+0.50)
```

### Sad But High Energy Output

```text
Profile: Sad But High Energy
Preferences:
Genre: pop
Mood: sad
Target Energy: 0.9
Target Valence: 0.2
Target Tempo: 130 BPM

Top 5 Recommendations:

1. Gym Hero
Score: 4.37
Reasons:
- genre match (+2.0)
- energy close to target (+0.97)
- valence close to target (+0.43)
- tempo close to target (+0.97)

2. Sunrise City
Score: 4.08
Reasons:
- genre match (+2.0)
- energy close to target (+0.92)
- valence close to target (+0.36)
- tempo close to target (+0.80)

3. Neon Horizon
Score: 2.37
Reasons:
- energy close to target (+0.95)
- valence close to target (+0.45)
- tempo close to target (+0.97)

4. Storm Runner
Score: 2.34
Reasons:
- energy close to target (+0.99)
- valence close to target (+0.72)
- tempo close to target (+0.63)

5. Night Drive Loop
Score: 2.23
Reasons:
- energy close to target (+0.85)
- valence close to target (+0.71)
- tempo close to target (+0.67)
```

### Genre Mismatch Test Output

```text
Profile: Genre Mismatch Test
Preferences:
Genre: classical
Mood: happy
Target Energy: 0.8
Target Valence: 0.9
Target Tempo: 120 BPM

Top 5 Recommendations:

1. Sunrise City
Score: 3.89
Reasons:
- mood match (+1.0)
- energy close to target (+0.98)
- valence close to target (+0.94)
- tempo close to target (+0.97)

2. Rooftop Lights
Score: 3.80
Reasons:
- mood match (+1.0)
- energy close to target (+0.96)
- valence close to target (+0.91)
- tempo close to target (+0.93)

3. Winter Nocturne
Score: 2.75
Reasons:
- genre match (+2.0)
- energy close to target (+0.35)
- valence close to target (+0.40)
- tempo close to target (+0.00)

4. Neon Horizon
Score: 2.57
Reasons:
- energy close to target (+0.85)
- valence close to target (+0.85)
- tempo close to target (+0.87)

5. Gym Hero
Score: 2.54
Reasons:
- energy close to target (+0.87)
- valence close to target (+0.87)
- tempo close to target (+0.80)
```

---

## Intended Use

This system is intended for a class project and for learning how recommendation
systems work. It is useful for showing how song features can be compared to a user's
preferences to make a ranked list. It is meant for classroom exploration, not for real
users.

---

## Non-Intended Use

- It should not be used as a real commercial music recommendation product.
- It should not be used to judge artists or predict how popular a song will be.
- It should not be treated as fully accurate, because it is small and simple.
- It should not replace the real recommendation systems used by music apps.

---

## Ideas for Improvement

- Add more songs and more genres so the recommender has more variety.
- Use real user behavior like likes, skips, saves, and playlists so it can learn over time.
- Let the user change the weights, or make the system avoid recommending the same song too often.

---

## Personal Reflection

My biggest learning moment was understanding that a recommender does not magically know
what someone likes. It needs data, rules, and a way to compare each song to a user
profile. Using AI tools helped me understand the code and write the scoring logic, and
it explained things in simple words when I was confused. But I still had to check the
AI's work, especially when I looked at the results to see if the top songs actually
matched each profile, and when I made sure the weights went back to normal after my
experiment. I was surprised that such a simple scoring system could still feel like a
real recommendation, because the top songs usually matched the user's vibe. If I kept
working on this project, I would add more songs and let users give feedback like likes
and skips, so the system could get better over time instead of only using the profile.
