# 🎵 Music Recommender Simulation

## Project Summary

This project is a small music recommender that I built for class. It reads a list of
songs from a CSV file and compares each song to a user's taste profile (their favorite
genre, mood, and target energy, valence, and tempo). It gives every song a score, ranks
them from best match to worst, and shows the top few with reasons for why each song was
picked. It uses content-based filtering, which means it recommends songs based on the
song's own features, not on what other users liked. I also added some optional features
like extra song attributes, different scoring modes, and a diversity penalty.

---

## How The System Works

### How real music apps do it

Real music apps like Spotify and YouTube look at a huge amount of data about what
people do — what they play, like, skip, and add to playlists. They use two main ideas.
The first is **collaborative filtering**, which finds people with similar taste and
suggests songs those people liked. The second is **content-based filtering**, which
looks at the features of songs you already like and finds new songs that feel similar.
Big apps usually mix both to get better results.

### How my simple version works

My version is much smaller. It only uses **content-based filtering**. It takes a user's
taste profile and gives every song a score based on how well the song matches. It cares
most about matching the user's favorite genre, then mood, then how close the song's
energy, valence, and tempo are to what the user wants. After scoring every song, it
ranks them from best to worst and shows the top few. It does not know about other
users, lyrics, or listening history — just the song features in my data file.

### My Algorithm Recipe

Each song starts at 0 points, then earns points like this:

```
score(song) =
      2.0  if the song genre matches the user's favorite genre
    + 1.0  if the song mood matches the user's favorite mood
    + 1.0 * (1 - |song energy  - target energy|)
    + 1.0 * (1 - |song valence - target valence|)
    + 1.0 * (1 - |song tempo   - target tempo| / 60)   (never below 0)
```

Genre is worth the most because it is the biggest part of someone's taste. The number
features (energy, valence, tempo) give more points the **closer** the song is to what
the user wants, not just for being higher. After every song has a score, I **sort** them
from highest to lowest and show the top results.

### Data Flow

```text
Input:  User preferences (genre, mood, energy, valence, tempo)
   |
Process: Loop through every song in songs.csv
   |
Score:  Give each song points using the Algorithm Recipe
   |
Rank:   Sort songs from highest score to lowest score
   |
Output: Show the top recommendations (with reasons)
```

### Features my `Song` object uses

- `genre` (pop, lofi, rock, hip hop, etc.)
- `mood` (happy, chill, intense, etc.)
- `energy` (0 to 1)
- `valence` (how happy the song sounds, 0 to 1)
- `tempo_bpm` (how fast the beat is)
- `acousticness` (how acoustic it is, 0 to 1)
- (plus `id`, `title`, and `artist` which are just labels)

### Features my `UserProfile` object uses

- `favorite_genre` (the genre the user likes most)
- `favorite_mood` (the mood the user likes most)
- `target_energy` (how much energy they want, 0 to 1)
- `target_valence` (how happy they want the song, 0 to 1)
- `target_tempo` (the beat speed they want, in bpm)

### Possible bias or weakness

This system might **over-prioritize genre**, so it could miss songs that match the
user's mood or energy but are from a different genre. For example, a chill, low-energy
song a user would love could get skipped just because it is labeled a different genre.
It also only works on a tiny catalog and does not understand lyrics or language.

---

## Optional Features Added

I added extra song features such as popularity, release decade, instrumentalness,
detailed mood, and language (danceability and acousticness were already there). I also
added multiple scoring modes (`balanced`, `genre_first`, `mood_first`, and
`energy_focused`) so the recommender can rank songs in different ways using a simple
Strategy pattern. A diversity penalty (that I can turn on or off) helps avoid
recommending too many songs from the same artist or genre. Finally, the terminal output
now shows recommendations in a cleaner table format with the reasons listed underneath.

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

Running `python -m src.main` prints a few demos in a table format: one using the
`energy_focused` scoring mode, and one profile shown with the diversity penalty off and
then on. Below is the first demo as an example. (Full evaluation output for five
profiles is in [model_card.md](model_card.md).)

```text
Loaded songs: 18

============================================================
Profile: High-Energy Pop
Scoring Mode: energy_focused
Diversity: off

Rank | Title            | Artist        | Genre     | Mood      | Score
-----+------------------+---------------+-----------+-----------+------
1    | Gym Hero         | Max Pulse     | pop       | intense   | 10.03
2    | Sunrise City     | Neon Echo     | pop       | happy     | 9.84
3    | Neon Horizon     | Pulse Theory  | edm       | energetic | 8.54
4    | Rooftop Lights   | Indigo Parade | indie pop | happy     | 8.29
5    | City Lights Flow | MC Vero       | hip hop   | confident | 8.09

Reasons:
1. Gym Hero
   - genre match (+1.0)
   - detailed mood match (+0.5)
   - decade match (+0.5)
   - energy close to target (+2.91)
   - valence close to target (+0.43)
   - tempo close to target (+1.77)
   - danceability close to target (+1.94)
   - acousticness close to target (+0.47)
   - popular enough (+0.50)
2. Sunrise City
   - genre match (+1.0)
   - mood match (+0.5)
   - decade match (+0.5)
   - energy close to target (+2.76)
   - valence close to target (+0.47)
   - tempo close to target (+1.77)
   - danceability close to target (+1.88)
   - acousticness close to target (+0.46)
   - popular enough (+0.50)
```

Note: scores in `energy_focused` mode can go above 5 because that mode stacks several
high weights (energy, tempo, and danceability). Scores are only meant to be compared
within the same scoring mode.

---

## Experiments You Tried

- **Weight shift experiment:** I changed genre from +2.0 down to +1.0 and energy from
  up to +1.0 up to +2.0. The #1 song for each profile stayed the same, but lower ranks
  started favoring high-energy songs from other genres (a rock song even jumped into the
  pop list). This showed me energy became stronger and genre became weaker.
- **Different user types:** I tested High-Energy Pop, Chill Lofi, Deep Intense Rock, and
  two edge cases (Sad But High Energy, Genre Mismatch Test). Each profile got songs that
  mostly matched its vibe. Full results are in [model_card.md](model_card.md).
- **Scoring modes:** I compared `genre_first` and `energy_focused`. In `genre_first`,
  lofi songs swept the top because a genre match is worth +4.0. In `energy_focused`,
  high-energy songs took over.

---

## Limitations and Risks

- It only works on a tiny catalog (18 songs), so there is not much variety.
- It does not understand lyrics or language, just the numbers and labels in the data.
- It can over-favor genre, so it might miss a song from a different genre that matches
  the user's mood and energy really well.
- The same song can show up for many profiles (like "Gym Hero" for high-energy tastes).
- It does not use real user behavior like likes, skips, saves, or playlists.

I go deeper on these in the [model card](model_card.md).

---

## Reflection

Working on this project taught me that a recommender does not magically know what
someone likes. It needs data, rules, and a way to compare each song to a user profile.
I learned that turning data into predictions is really just giving each song a score
from simple rules and then sorting the scores. It was cool to see that a simple scoring
system could still feel like a real recommendation when the top songs matched the user's
vibe.

I also saw where bias can show up. Because genre is worth the most points, the system
can get stuck recommending one genre and create a small filter bubble. And because my
data is small and missing some moods (like there is no "sad" song), the system does
badly for those tastes. A real app would need way more data and would need to be careful
that it does not unfairly ignore certain artists, genres, or listeners.

See the full model card here: [**Model Card**](model_card.md)



