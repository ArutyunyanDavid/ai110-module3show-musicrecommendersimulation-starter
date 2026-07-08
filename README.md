# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

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

This is the real terminal output from running `python -m src.main`:

```text
Loaded songs: 18

User Profile:
Genre: pop
Mood: happy
Target Energy: 0.8
Target Valence: 0.9
Target Tempo: 120 BPM

Top Recommendations:

1. Sunrise City
Score: 5.89
Reasons:
- genre match (+2.0)
- mood match (+1.0)
- energy close to target (+0.98)
- valence close to target (+0.94)
- tempo close to target (+0.97)

2. Gym Hero
Score: 4.54
Reasons:
- genre match (+2.0)
- energy close to target (+0.87)
- valence close to target (+0.87)
- tempo close to target (+0.80)

3. Rooftop Lights
Score: 3.80
Reasons:
- mood match (+1.0)
- energy close to target (+0.96)
- valence close to target (+0.91)
- tempo close to target (+0.93)

4. Neon Horizon
Score: 2.57
Reasons:
- energy close to target (+0.85)
- valence close to target (+0.85)
- tempo close to target (+0.87)

5. City Lights Flow
Score: 2.38
Reasons:
- energy close to target (+1.00)
- valence close to target (+0.80)
- tempo close to target (+0.58)
```

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



