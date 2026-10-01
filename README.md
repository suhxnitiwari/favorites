# Favorites

Everything from [suhanitiwari.com/home/favorites](https://suhanitiwari.com/home/favorites) as open, structured data: the shows, movies, TED talks and books I love, plus a snapshot of my Spotify listening.

**Live page:** https://suhxnitiwari.github.io/favorites/

## What's inside

| File | What it holds |
|---|---|
| [`data/watch.json`](data/watch.json) | TV shows, movies, Desi picks and comedy specials, grouped into shelves |
| [`data/inspiration.json`](data/inspiration.json) | 26 TED / TEDx talks by topic, with YouTube links and why I watch each topic |
| [`data/read.json`](data/read.json) | Books: how things work, how people work, how I want to live |
| [`data/listen.json`](data/listen.json) | What my Spotify says about me |
| [`data/music/`](data/music) | Spotify snapshot: top tracks, top artists, top genres, recently played, short/medium/long-term history |
| [`data/my-type.json`](data/my-type.json) | The three threads that tie it all together |
| [`images/`](images) | Posters, book covers and talk thumbnails |
| [`index.html`](index.html) | A small page that renders all of the above |

## Refresh the data

```bash
python3 scripts/scrape.py
```

No dependencies: the script only uses the Python standard library. It re-reads the live page and Spotify endpoints and rewrites `data/`.

To preview locally:

```bash
python3 -m http.server 8000
```

## Quick look

### Shows I Rewatch on Repeat
_For sad days, lazy days, and the days I feel like a hopeless couch-potato blob. These always make me a little happier._

- Gossip Girl (2007–2012)
- Jane the Virgin (2014–2019)
- Modern Family (2009–2020)
- Friends (1994–2004)
- Desperate Housewives (2004–2012)

### Romance Movies That I'm In Love With
_For nights when I’m feeling a little delusional, hopelessly romantic, and in need of a happy ending._

- Yeh Jawaani Hai Deewani (2013)
- How to Lose a Guy in 10 Days (2003)
- Jab We Met (2007)
- Voicemails for Isabelle (2026)
- Tu Jhoothi Main Makkaar (2023)
- Rocky Aur Rani Kii Prem Kahaani (2023)
- Student of the Year (2012)

### The Desi Edit
- Don't Be Shy (2026 film)
- Dil Dosti Dilemma (2024)
- Call Me Bae (2024)
- Mind the Malhotras (2019)
- Mismatched (2020–)
- Masaba Masaba (2020–2022)

### Watched It, Loved It, Moved On
- Gilmore Girls (2000–2007)
- Ginny & Georgia (2021–)
- Bridgerton (2020–)
- 56 Days (2026)
- Off Campus (2026–)

### Comedy That Never Misses
- Zakir Khan: Papa Yaar (Stand-up special)
- Amit Tandon: Family Tandoncies (Stand-up special)
- Hasan Minhaj: Homecoming King (Stand-up special)
- Ladies Up (Stand-up series)
- The Great Indian Kapil Show (2024–)

### Books Behind the Business
- Onward: How Starbucks Fought for Its Life Without Losing Its Soul (Howard Schultz)
- The Design of Everyday Things (Don Norman)
- Inspired (Marty Cagan)
- Creative Confidence (Tom Kelley & David Kelley)
- The Innovator's Dilemma (Clayton Christensen)
- Competing Against Luck (Clayton Christensen)
- Shoe Dog (Phil Knight)
- Creativity, Inc. (Ed Catmull)
- Alchemy (Rory Sutherland)
- The Choice Factory (Richard Shotton)
- Decoded (Phil Barden)
- Influence (Robert Cialdini)

### Books I’ll Never Shut Up About
_Enemies to lovers, fake dating and happy endings: I know how every one ends and still can’t put them down._

- The Hating Game (Sally Thorne)
- The Unhoneymooners (Christina Lauren)
- People We Meet on Vacation (Emily Henry)
- You Deserve Each Other (Sarah Hogle)
- The Spanish Love Deception (Elena Armas)
- By a Thread (Lucy Score)
- The Devil You Know (Elizabeth O'Roark)
- The Ex Talk (Rachel Lynn Solomon)
- Funny Story (Emily Henry)
- The American Roommate Experiment (Elena Armas)
- The Worst Best Man (Mia Sosa)
- The Love Hypothesis (Ali Hazelwood)

### Books That Actually Changed How I Live
_Atomic Habits made me trust systems, Let Them ended my overthinking, and Carnegie is why I remember your coffee order._

- Atomic Habits (James Clear)
- The Let Them Theory (Mel Robbins)
- How to Win Friends and Influence People (Dale Carnegie)
- Ikigai (Héctor García & Francesc Miralles)
- The 48 Laws of Power (Robert Greene)

### Comfort TED talks
- [Change Your Mindset, Change the Game](https://www.youtube.com/watch?v=0tqq66zwa7g): Alia Crum, TEDx
- [You Aren’t at the Mercy of Your Emotions: Your Brain Creates Them](https://www.youtube.com/watch?v=0gks6ceq4eQ): Lisa Feldman Barrett, TED
- [How to Make Learning as Addictive as Social Media](https://www.youtube.com/watch?v=P6FORpg0KVo): Luis von Ahn, TED
- [Education Reimagined: Student-Led Learning](https://www.youtube.com/watch?v=NTHBdIeV-8o): Catlin Tucker, TEDx
- [Creativity in the Classroom (in 5 Minutes or Less!)](https://www.youtube.com/watch?v=nASvIgSOCxw): Catherine Thimmesh, TEDx
- [How to Design a Library That Makes Kids Want to Read](https://www.youtube.com/watch?v=YsA_JTeHJ6A): Michael Bierut, TED
- [Every Kid Needs a Champion](https://www.youtube.com/watch?v=SFnMTHhKdkw): Rita Pierson, TED
- [The Child-Driven Education](https://www.youtube.com/watch?v=nsKPvQCMATw): Sugata Mitra, TED
- [Do Schools Kill Creativity?](https://www.youtube.com/watch?v=iG9CE55wbtY): Sir Ken Robinson, TED
- [Your Elusive Creative Genius](https://www.youtube.com/watch?v=86x-u-tz0MA): Elizabeth Gilbert, TED
- [4 Lessons in Creativity](https://www.youtube.com/watch?v=sY0Pf_pfqCI): Julie Burstein, TED
- [Tales of Creativity and Play](https://www.youtube.com/watch?v=RjwUn-aA0VY): Tim Brown, TED
- [Designers, Think Big!](https://www.youtube.com/watch?v=UAinLaT42xY): Tim Brown, TED
- [Success, Failure and the Drive to Keep Creating](https://www.youtube.com/watch?v=_waBFUg_oT8): Elizabeth Gilbert, TED
- [The Power of Believing That You Can Improve](https://www.youtube.com/watch?v=_X0mgOOSpLU): Carol Dweck, TED
- [Grit: The Power of Passion and Perseverance](https://www.youtube.com/watch?v=H14bBuluwB8): Angela Lee Duckworth, TED
- [How Every Child Can Thrive by Five](https://www.youtube.com/watch?v=aISXCw0Pi94): Molly Wright, TED
- [What Makes a Good Life?](https://www.youtube.com/watch?v=8KkKuTCFvzI): Robert Waldinger, TED
- [There’s More to Life Than Being Happy](https://www.youtube.com/watch?v=y9Trdafp83U): Emily Esfahani Smith, TED
- [How Airbnb Designs for Trust](https://www.youtube.com/watch?v=16cM-RFid9U): Joe Gebbia, Airbnb co-founder, TED
- [How to Build the Future in Four Steps](https://www.youtube.com/watch?v=EMiJMod9vsk): Jason Kilar, Hulu founding CEO, TEDx
- [How to Connect While Apart](https://www.youtube.com/watch?v=01qATwnoD_E): Eric Yuan, Zoom founder, TED
- [Choice, Happiness and Spaghetti Sauce](https://www.youtube.com/watch?v=iIiAAhUeR6Y): Malcolm Gladwell, TED
- [How to Make Choosing Easier](https://www.youtube.com/watch?v=1pq5jnM1C-A): Sheena Iyengar, TED
- [How to Get Your Ideas to Spread](https://www.youtube.com/watch?v=xBIVlM435Zg): Seth Godin, TED
- [The Paradox of Choice](https://www.youtube.com/watch?v=VO6XEQIsCoM): Barry Schwartz, TED

---
© 2026 Suhani Tiwari. All rights reserved. Posters, covers and thumbnails belong to their respective owners.
