# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

One limitation I found is that the system can over-prioritize genre. If a song
matches the user's favorite genre it gets a big +2.0 boost, so a song from a
different genre can get skipped even if its mood, energy, and tempo are a better
match. This can create a kind of filter bubble where the user mostly gets songs
from the one genre they already picked. My dataset is also pretty small (only 18
songs), so a few songs keep showing up across different profiles — for example
"Gym Hero" appeared in the top 5 of four of my five profiles because it is pop
with very high energy. Some genres and moods are also underrepresented (there is
only one classical song and no "sad" song at all), so the system does badly for
users who want those. Finally, my recommender does not use any real user behavior
like skips, likes, saves, or playlists, so it can't learn or improve over time
like a real app would.

---

## 7. Evaluation  

### Profiles I tested and what each one was checking

| Profile | What it was testing |
|---|---|
| **High-Energy Pop** | A clear, "easy" taste where genre, mood, and numbers all point the same way. |
| **Chill Lofi** | A low-energy, slow-tempo taste (the opposite of the pop profile). Its mood was "calm", which is NOT a mood in my data, so it tests what happens when the mood label doesn't exist. |
| **Deep Intense Rock** | A high-energy but low-valence (darker) taste to see if it picks rock/intense songs. |
| **Sad But High Energy** (edge case) | A tricky profile that asks for two things that usually don't go together: sad (low valence) but high energy. Tests mixed/conflicting preferences. |
| **Genre Mismatch Test** (edge case) | Asks for "classical", a genre with only one song in my data. Tests what happens when the favorite genre barely exists. |

### Did the results make sense?

Mostly yes. Pop/happy songs topped the pop profile, lofi songs topped the lofi
profile, and Storm Runner (rock/intense) topped the rock profile. The edge cases
behaved in ways that made sense once I looked at the scores.

### What surprised me

- **The same song kept showing up.** "Gym Hero" (pop, energy 0.93) appeared in the
  top 5 of four different profiles, just because so many of my profiles wanted high
  energy.
- **Genre is powerful, but not always.** For Chill Lofi, the whole top 3 were lofi
  songs because of the genre boost. But for Genre Mismatch Test, the only classical
  song did NOT win — its numbers were so far off that a well-matching pop song beat
  it. So genre is strong but can still lose.
- **The "sad" profile couldn't really get sad songs.** Because no song in my data has
  a "sad" mood, and the top picks were upbeat pop songs. The genre + energy + tempo
  points beat the low-valence request.

### Comparisons between profiles

- The **High-Energy Pop** profile preferred upbeat songs because it had high target
  energy, high valence, and a pop genre preference.
- The **Chill Lofi** profile shifted toward calmer, slower songs because it had low
  energy and a slow target tempo — basically the opposite of the pop profile.
- The **Deep Intense Rock** profile preferred louder, faster songs because it had
  high energy, low valence, and a rock genre preference.
- The **Sad But High Energy** profile was interesting because it asked for two
  conflicting things (sad mood but high energy), which helped test whether the
  recommender could handle mixed preferences. It ended up choosing high-energy pop
  songs and mostly ignoring the "sad" part.
- The **Genre Mismatch Test** profile showed that when a favorite genre barely exists,
  the recommender falls back on mood and the numeric features instead.

### My weight experiment (Option A: Weight Shift)

I changed the weights so genre went from +2.0 down to +1.0, and energy went from up
to +1.0 up to +2.0. (To reproduce: set `WEIGHT_GENRE = 1.0` and `WEIGHT_ENERGY = 2.0`
in `src/recommender.py`.)

What happened: the #1 song for each profile stayed the same, but the lower ranks
started favoring high-energy songs from OTHER genres. In High-Energy Pop, the rock
song "Storm Runner" climbed into the top 5. In Genre Mismatch Test, the single
classical song fell out of the top 5 completely. So the change made the results
**different and a bit worse for staying on-genre** — it showed that energy became
more powerful and genre became weaker.

### Terminal output for each profile

These are the real outputs from `python -m src.main` (baseline weights).

#### High-Energy Pop Output

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

#### Chill Lofi Output

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

#### Deep Intense Rock Output

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

#### Sad But High Energy Output

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

#### Genre Mismatch Test Output

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

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
