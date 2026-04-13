# 🎵 Music Recommender Simulation

## Project Summary

VibeFinder 1.0 is a content-based music recommender simulation
built in Python. It takes a user taste profile (favorite genre,
mood, and target audio features) and scores every song in a
small catalog to return the top 5 best matches. Each
recommendation includes a plain-language explanation of why
that song was suggested. The project demonstrates how real
platforms like Spotify use weighted scoring to turn user
preferences into personalized suggestions.

---

## How The System Works

Each Song in the system stores: title, artist, genre, mood,
energy (0.0–1.0), valence (0.0–1.0), danceability (0.0–1.0),
acousticness (0.0–1.0), and tempo in BPM.

The UserProfile stores: favorite genre, favorite mood, and
target values for energy, valence, danceability, acousticness,
and tempo.

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

Maximum possible score: 100 points

Expected bias: Genre match dominates scoring (50/100 points),
so non-pop songs are unlikely to appear even with strong
numerical feature matches.



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

## Experiments You Tried

**Experiment 1 — Default weights (genre: 50, energy: 8):**
The High Energy Pop profile correctly surfaced Sunrise City
at 100 points. The Chill Lofi profile surfaced Library Rain
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

---

## Limitations and Risks

- The catalog only has 18 songs, which severely limits
  variety especially for less common genres like rock or
  classical.
- Genre matching accounts for 50% of the total score,
  creating a filter bubble where users rarely see songs
  outside their stated genre.
- The system does not consider lyrics, language, release
  year, artist familiarity, or listening history.
- Moods that are underrepresented in the dataset (like sad
  or angry) produce poor results because there are simply
  not enough matching songs.
- The scoring treats all users as having the same preference
  shape — there is no way to say "genre matters more to me
  than energy."

---

## Reflection

Read and complete `model_card.md`:

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


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

