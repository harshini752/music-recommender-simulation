# 🎵 Music Recommender Simulation

## Project Summary
VibeFinder 1.0 is a content-based music recommender simulation
built in Python. It takes a user taste profile (favorite genre,
mood, and target audio features) and scores every song in a
small catalog to return the top 5 best matches. Each
recommendation includes a plain-language explanation of why
that song was suggested. The project demonstrates how real
platforms like Spotify use weighted scoring to turn user
preferences into personalized suggestions. It also includes
four optional extensions: advanced song features, multiple
scoring modes, an artist diversity penalty, and visual table
output using tabulate.

---

## How The System Works
Each Song in the system stores: title, artist, genre, mood,
energy (0.0–1.0), valence (0.0–1.0), danceability (0.0–1.0),
acousticness (0.0–1.0), tempo in BPM, speechiness,
instrumentalness, popularity (0–100), release decade, and
mood tag.

The UserProfile stores: favorite genre, favorite mood, mood
tag, and target values for energy, valence, danceability,
acousticness, and tempo.

The Recommender scores each song by checking how well it
matches the user profile. Genre and mood are binary checks
worth the most points. Audio features like energy, valence,
and danceability use a proximity formula — songs closer to
the user's target value score higher than songs that are
far away. All scores are sorted highest to lowest and the
top K songs are returned with explanations.

## System Flowchart

```mermaid
graph TD
    A[User Preferences] --> B[Start loop through songs CSV]
    B --> C[score_song()]
    C --> D[Check genre match]
    D --> E[Check mood match]
    E --> F[Check energy/valence/danceability proximity]
    F --> G[Calculate total score]
    G --> H{More songs?}
    H -->|Yes| C
    H -->|No| I[Sort all songs by score]
    I --> J[Return top K recommendations]
```

## Algorithm Recipe

- +50 points → Genre exact match
- +30 points → Mood exact match
- +8 points  → Energy proximity (difference ≤ 0.1)
- +4 points  → Energy proximity (difference ≤ 0.2)
- +2 points  → Energy proximity (difference ≤ 0.3)
- +6 points  → Valence proximity (difference ≤ 0.1)
- +3 points  → Valence proximity (difference ≤ 0.2)
- +1 point   → Valence proximity (difference ≤ 0.3)
- +6 points  → Danceability proximity (difference ≤ 0.1)
- +3 points  → Danceability proximity (difference ≤ 0.2)
- +1 point   → Danceability proximity (difference ≤ 0.3)
- +5 points  → Song popularity ≥ 85
- +3 points  → Song popularity ≥ 70
- +4 points  → Mood tag exact match

Maximum possible score: 109 points

Expected bias: Genre match dominates scoring (50/109 points),
so non-matching genre songs rarely appear even when other
features are a strong match.

---

## Optional Extensions Completed

**Challenge 1 — Advanced Song Features:**
Added popularity (0–100), release_decade, mood_tag, speechiness,
and instrumentalness to songs.csv. Scoring now rewards highly
popular songs and exact mood tag matches.

**Challenge 2 — Multiple Scoring Modes:**
Three additional modes available via the mode parameter in
recommend_songs():
- genre_first — genre worth 70 points, mood 20, numerics reduced
- mood_first — mood worth 60 points, genre 20, valence boosted
- energy_focused — energy worth up to 40 points, genre/mood reduced

**Challenge 3 — Diversity Penalty:**
Added apply_diversity_penalty() which detects if an artist
appears more than once in the natural top 3 results and
subtracts 1.5 points from their duplicate songs before the
final sort. Enable with diversity=True in recommend_songs().

**Challenge 4 — Visual Table Output:**
Added print_table() using the tabulate library. All profiles
now display as formatted tables showing Rank, Title, Artist,
Genre, Score, and Top Reason.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):
```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
   pip install tabulate
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

## Experiments You Tried

**Experiment 1 — Default weights (genre: 50, energy: 8):**
The High Energy Pop profile correctly surfaced Sunrise City
at 109 points. The Chill Lofi profile surfaced Library Rain
and Midnight Coding. Results matched intuition well for
users whose genre was well represented in the catalog.

**Experiment 2 — Adversarial profile (sad mood + high energy + pop):**
When mood had no matches in the catalog, the system ignored
mood entirely and ranked songs purely by genre and energy.
Gym Hero ranked first despite not being sad at all. This
exposed a clear genre dominance bias.

**Experiment 3 — Halved genre weight (25) and doubled energy weight (16):**
Results became more diverse. A rock song appeared in the
pop profile results for the first time. The Chill Lofi
profile shifted Spacewalk Thoughts from #4 to #3 based
purely on energy proximity. However overall accuracy
dropped for users with strong genre preferences.

**Experiment 4 — Scoring mode comparison (Challenge 2):**
Running the same High Energy Pop profile through all three
modes produced noticeably different rankings. Energy-focused
mode surfaced songs from different genres that happened to
match the energy target, showing how much a single weight
decision shapes the entire output.

**Experiment 5 — Diversity penalty (Challenge 3):**
The Chill Lofi profile without diversity showed LoRoom
appearing twice in the top 3 (Midnight Coding and Focus Flow).
With diversity enabled, Focus Flow dropped from 68.00 to
66.50 due to the penalty, creating more artist variety.

---

## Limitations and Risks

- The catalog only has 18 songs, which severely limits
  variety especially for less common genres like rock or
  classical.
- Genre matching accounts for 50% of the base score,
  creating a filter bubble where users rarely see songs
  outside their stated genre.
- The system does not consider lyrics, language, or
  listening history.
- Moods that are underrepresented in the dataset (like sad
  or angry) produce poor results because there are simply
  not enough matching songs.
- The scoring treats all users as having the same preference
  shape — there is no way to say genre matters more to me
  than energy without switching modes manually.

---

## Reflection

[**Model Card**](model_card.md)

Building this recommender taught me that every design
decision in a scoring system has consequences for which
users get good results and which ones do not. Assigning
50 points to genre seemed reasonable at first, but testing
revealed it essentially made genre the only thing that
mattered. This mirrors how real platforms can trap users
in filter bubbles — not out of malice, but because of
weighted math that quietly favors certain preferences.

The most surprising moment was the adversarial profile
test. I expected broken or random output but instead got
a clear and explainable pattern: genre always wins. That
realization changed how I think about apps like Spotify.
What feels like magic is actually a series of human
engineering decisions baked into weights and thresholds.
Understanding that makes me more curious and more
skeptical every time an algorithm tells me what to listen
to next.