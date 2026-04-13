# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name
VibeFinder 1.0

---

## 2. Intended Use
VibeFinder 1.0 is designed to suggest songs from a small
catalog based on a user's musical taste profile. It is
built for classroom exploration and learning purposes,
not for real-world deployment.

The model assumes the user can describe their preferences
using a genre (like pop or rock), a mood (like happy or
chill), and numerical targets for audio features like
energy and danceability. It is intended for students and
developers who want to understand how content-based
recommendation systems work under the hood.

---

## 3. How the Model Works
The model works by giving every song in the catalog a
score based on how well it matches the user's preferences,
then returning the top 5 highest-scoring songs.

For each song, the system checks a few things. First, does
the song's genre match the user's favorite genre? If yes,
it gets 50 points. Does the mood match? That adds 30 more
points. Then the system looks at audio features like energy,
valence, and danceability. Instead of just rewarding high
or low values, it rewards songs that are close to what the
user actually wants. For example, if you want medium energy
(0.8), a song with energy 0.82 scores much better than one
with energy 0.3. The closer the match, the more points.

The original starter logic had no scoring at all — just
placeholder functions. I designed the full scoring recipe
from scratch, added valence and danceability proximity on
top of the basic genre and mood checks, and built an
explanation system that tells you exactly why each song
was recommended.

---

## 4. Data
The catalog contains 18 songs stored in a CSV file. Each
song has the following attributes: title, artist, genre,
mood, energy, valence, danceability, acousticness, and
tempo in BPM.

The genres represented include pop, lofi, rock, electronic,
reggae, and classical. Moods include happy, chill, intense,
melancholic, and energetic.

I expanded the original 10-song dataset by adding 8 more
songs to improve diversity. However, the dataset is still
heavily weighted toward pop and lofi, with only one or two
songs representing genres like rock or classical. Features
like lyrics, language, release year, and listening history
are completely absent, which limits how well the system
can capture real musical taste.

---

## 5. Strengths
The system works best when the user's preferences closely
match a well-represented genre in the catalog. For example,
the High Energy Pop and Chill Lofi profiles both produced
very accurate and intuitive top results.

The scoring logic correctly separates very different vibes.
A chill lofi profile and a high energy pop profile produce
completely opposite recommendation lists, which is exactly
what you would expect. The explanation feature is also a
strength — every recommendation comes with a clear reason,
which makes the system easy to understand and debug.

---

## 6. Limitations and Bias
The biggest limitation is that genre matching accounts for
50 out of 100 possible points. This means genre almost
always dominates the final ranking, even when other features
like mood or energy are a better match. A pop song with the
wrong mood will consistently outrank a perfect mood match
from a different genre.

The dataset is also unbalanced. Pop and lofi make up the
majority of songs, so users who prefer rock, jazz, or
classical will receive weaker and less varied recommendations
simply because there are fewer songs available for them.

The adversarial test profile (sad mood + high energy + pop)
exposed another bias — when no songs match the requested
mood, the mood preference is completely ignored and genre
takes over entirely. The system has no way to handle
conflicting preferences gracefully.

Features like lyrics, tempo range preferences, release
decade, and listening history are not considered at all.

---

## 7. Evaluation
I tested four user profiles: High Energy Pop, Chill Lofi,
Deep Intense Rock, and an Adversarial profile with
conflicting preferences (sad mood combined with high energy
and pop genre).

For High Energy Pop and Chill Lofi, the top results matched
my intuition perfectly. For Deep Intense Rock, the system
found Storm Runner as a strong match but struggled to fill
the remaining spots since only one rock song existed in the
catalog.

The most surprising result came from the Adversarial profile.
I expected random or broken output, but instead the system
consistently surfaced pop songs based on genre alone,
completely ignoring the sad mood preference. This clearly
demonstrated the genre dominance bias.

I also ran a weight experiment where I halved the genre
weight from 50 to 25 and doubled the energy weight from 8
to 16. This produced more diverse results — a rock song
appeared in the pop list for the first time — but reduced
overall accuracy for users with strong genre preferences.

---

## 8. Future Work
1. Add collaborative filtering by incorporating listening
   history so the system can learn from what users actually
   skip or replay, not just their stated preferences.
2. Expand the dataset to at least 200 songs with balanced
   genre and mood representation so every user type gets
   meaningful variety in their top 5.
3. Add a diversity penalty so the same artist or genre
   cannot appear more than twice in the top 5 results,
   preventing the system from over-recommending one style.
4. Replace fixed weights with user-adjustable sliders so
   a user can say genre matters more to them than energy,
   making the system truly personalized.

---

## 9. Personal Reflection
Building VibeFinder taught me that even the simplest
recommendation system involves real design decisions with
real consequences. Choosing how many points to assign to
genre versus energy is not just math — it shapes whose
taste the system serves well and whose it ignores.

The most unexpected discovery was how clearly a 50-point
genre weight created a filter bubble. I assumed the system
would feel balanced, but testing it showed that genre was
essentially the only thing that mattered for most profiles.
That surprised me because in real life I often discover
great songs outside my usual genre.

This project changed how I think about apps like Spotify.
What feels like magic is actually a series of weighted
decisions made by engineers, and those decisions embed
assumptions about what users care about. Understanding
that makes me more curious and more skeptical every time
an algorithm tells me what I should listen to next.