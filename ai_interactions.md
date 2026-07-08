# AI Interactions

I used an AI coding assistant (Claude) inside VS Code to help me build the optional
challenge features. I asked it to keep the code beginner-friendly and to explain the
changes so I could understand and defend them.

## Challenge 1: Advanced Song Features

### Prompt Used
I asked the AI to add 5 or more new features to `data/songs.csv` (things like
popularity, release decade, instrumentalness, detailed mood, and language), keep all
the existing songs, fill in realistic values, and then update the scoring so it could
use some of the new features. I also asked it to make sure `load_songs` converted the
new numeric columns.

### AI Changes
- `data/songs.csv`: added 5 new columns — `instrumentalness`, `popularity`, `release_decade`, `detailed_mood`, and `language` — and filled in values for all 18 songs. (`danceability` and `acousticness` were already there.)
- `src/recommender.py`: updated `load_songs` to turn the new number columns (`instrumentalness`, `popularity`, `release_decade`) into real numbers, and to skip any column that is missing or blank so it does not crash.
- `src/recommender.py`: updated `score_song` so it can give points for danceability, acousticness, popularity, release decade, and detailed mood.

### Manual Verification
I ran `python -m src.main`. It printed "Loaded songs: 18", so all songs still loaded.
I also saw the new features show up in the reason lists (like "danceability close to
target" and "decade match"), which told me the numbers converted correctly and the
scoring was actually using them.

## Challenge 2: Multiple Scoring Modes

### Prompt Used
I asked the AI to add two or three scoring modes (like `genre_first`, `mood_first`, and
`energy_focused`) using a simple, beginner version of the Strategy pattern. I wanted to
keep one main `score_song` function and just store different weights in dictionaries,
and be able to call `recommend_songs(..., mode="genre_first")`.

### AI Changes
- Added a `SCORING_MODES` dictionary. Each mode is its own little dictionary of weights.
- `score_song` now takes a `mode` argument, looks up that mode's weights, and uses them. So the same function can rank songs in different ways without me writing a new function for each mode.
- `recommend_songs` also takes a `mode` argument and passes it down.
- `main.py` shows the scoring mode in the output header.

The Strategy pattern here is simple: the "strategy" is just which weight dictionary we
pick. `genre_first` makes genre worth a lot, `energy_focused` makes energy, tempo, and
danceability worth a lot, and so on.

### Manual Verification
I ran the program and compared modes. In `energy_focused`, high-energy songs like
"Gym Hero" and "Neon Horizon" jumped to the top. In `genre_first`, the lofi songs swept
the top 3 because a genre match is worth +4.0 in that mode. The lists were clearly
different, so the modes work.

## Challenge 3: Diversity and Fairness Logic

### Prompt Used
I asked the AI to add a simple diversity penalty so the top list does not have too many
songs from the same artist or genre. The rule: subtract 1.0 if an artist is already in
the list, and subtract 0.5 if a genre already shows up too much. I wanted to be able to
turn it on or off with `use_diversity=True`.

### AI Changes
- `recommend_songs` now has a `use_diversity` switch.
- When it is on, the program picks songs one at a time. Each time it picks a song, it lowers the score of any leftover song that repeats an artist or genre that was already chosen, then picks the next best one.
- The penalty is applied during ranking, not inside `score_song`. The AI explained why: one song's own score should not depend on which OTHER songs got picked — that is a property of the whole list, so it belongs in the ranking step.
- Penalty reasons show up in the output, like "diversity penalty: same artist already recommended (-1.0)".

### Manual Verification
I tested the "Chill Lofi" profile with diversity off and then on. With it off,
"Focus Flow" (by LoRoom) scored 7.88. With it on, its score dropped to 6.38 and the
reasons showed the artist and genre penalties, because another LoRoom song and other
lofi songs were already in the list. So the penalty works and the reasons explain it.

## Challenge 4: Visual Summary Table

### Prompt Used
I asked the AI to make the terminal output easier to read as a table, using only
built-in Python (no extra libraries to install). The table should show rank, title,
artist, genre, mood, and score, and print the reasons under each song if they are too
long for the table.

### AI Changes
- Added a `print_table` function in `main.py` that lines up the columns by measuring the widest value in each column and padding the others to match.
- It prints a header row, a divider line, then each song. The reasons are printed in a list under the table so they do not make the table messy.
- No new libraries are needed, so nothing extra has to be installed.

### Manual Verification
I ran `python -m src.main` and the table columns lined up neatly. Each song showed its
rank, title, artist, genre, mood, and score, with the reasons listed under it. It was
easy to read and easy to copy into my README.

---

## Agentic Workflow (SF8)

**What task did you give the agent?**

I asked it to complete four optional challenges in one go: add new song features,
add multiple scoring modes, add a diversity penalty, and make a table output. It made
changes across `data/songs.csv`, `src/recommender.py`, and `src/main.py`.

**Prompts used:**

The prompts are summarized in the "Prompt Used" parts of each challenge above.

**What did the agent generate or change?**

It edited the CSV to add 5 features, rewrote parts of `recommender.py` (load_songs,
score_song, recommend_songs, plus a SCORING_MODES dictionary and small helper
functions), and rewrote `main.py` to add the table and demo runs. It also ran the tests
and the program to check nothing broke.

**What did you verify or fix manually?**

I ran `python -m src.main` and `pytest` myself to confirm the songs loaded, the modes
gave different results, the diversity penalty showed up, and the old tests still passed.

## Design Pattern (SF10)

**Which design pattern did you use?**

A simple Strategy pattern.

**How did AI help you brainstorm or implement it?**

The AI suggested storing each scoring "strategy" as a dictionary of weights instead of
writing a separate function or class for each one. That kept it beginner-friendly.

**How does the pattern appear in your final code?**

In `src/recommender.py`, the `SCORING_MODES` dictionary holds the different weight sets,
and `score_song(user_prefs, song, mode)` picks the right one based on the `mode`. So the
"strategy" is just which weight dictionary gets used.
