"""Turn data/*.json into insights the website doesn't show.

Writes data/insights.json, INSIGHTS.md and exports/*.csv.
Usage: python3 scripts/analyze.py   (run after scrape.py)
"""
import csv, json, os, re
from collections import Counter
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda p: json.load(open(os.path.join(ROOT, "data", p)))
CENTRAL = timezone(timedelta(hours=-5))  # Austin (CDT)
TERMS = {"short_term": "last 4 weeks", "medium_term": "last 6 months", "long_term": "all time"}


def year(s):
    m = re.search(r"\d{4}", s or "")
    return int(m.group()) if m else None


# Indian, Pakistani and Punjabi artists, composers and lyricists that show up in my data.
DESI = set("""A.R. Rahman|AP Dhillon|Aaman Trikha|Aashir Wajahat|Aastha|Abhiruchi Chand|Achint|Aditi Singh Sharma|
Aditya Rikhari|Altamash Faridi|Amaal Mallik|Amit Trivedi|Amitabh Bhattacharya|Anand Raj Anand|Antara Mitra|
Anumita Nadesan|Anuv Jain|Arijit Singh|Arjun|Armaan Malik|Asees Kaur|Asha Bhosle|Atif Aslam|Badshah|Benny Dayal|
Bhargavi Pillai|Blaaze|Caralisa Monteiro|Chinmayi|DIVINE|Darshan Raval|Diljit Dosanjh|Dub Sharma|Guru Randhawa|
Harrdy Sandhu|Himesh Reshammiya|IP Singh|Jaani|Jaideep Sahni|Jasmine Sandlas|Jigar Saraiya|Jonita Gandhi|
Karan Aujla|Kumaar|Labh Janjua|Lijo George-Dj Chetas|Madhubanti Bagchi|Majrooh Sultanpuri|Meet Bros.|
Mohammad Faiz|Monali Thakur|Naresh Iyer|Neeraj Shridhar|Neeti Mohan|Neha Bhasin|Neha Kakkar|Nehaal Naseem|
Nikhil D'Souza|Nikhita Gandhi|Pragati Nagpal|Pritam|Priya Saraiya|QARAN|R. D. Burman|Raghav|Ranveer Singh|
Rashmeet Kaur|Rashmi Virag|Reble|Rochak Kohli|Sachet Tandon|Sachin-Jigar|Sanam Puri|Satish Chakravarthy|
Shadab Faridi|Shashwat Sachdev|Shilpa Rao|Shinda Kahlon|Shirley Setia|Shreya Ghoshal|Shreya Sharma|Simar Kaur|
Sonu Kakkar|Sumonto Mukherjee|Tanishk Bagchi|Tanvi Shah|The Doorbeen|Tulsi Kumar|Varun Grover|Vineet Singh|
Vishal Dadlani|Vishal Mishra|Vishal-Shekhar|Yo Yo Honey Singh|thiarajxtt""".replace("\n", "").split("|"))


# Desi titles outside "The Desi Edit" shelf
DESI_TITLES = ["Yeh Jawaani", "Jab We Met", "Tu Jhoothi", "Rocky Aur", "Student of the Year",
               "Zakir", "Amit Tandon", "Kapil", "Hasan Minhaj", "Ladies Up"]
# One-season shows the site lists with a single year
SINGLE_SEASON = {"Mind the Malhotras", "Dil Dosti Dilemma", "Call Me Bae", "56 Days"}


def is_desi(t):
    return any(a in DESI for a in t["artists"])


def music():
    lab = load("music/music-lab.json")
    tracks, artists, recent = lab["topTracks"], lab["topArtists"], lab["recent"]
    names = {term: [a["name"] for a in artists[term]] for term in TERMS}

    # Loyalty: artists in the top 15 of every time range
    ride_or_die = [a for a in names["long_term"][:15] if all(a in names[t][:15] for t in TERMS)]
    # Climbers: biggest jump from all-time rank to this month's rank (unranked counts as 51)
    rank = lambda term, a: names[term].index(a) + 1 if a in names[term] else 51
    climbers = sorted(({"name": a, "now": rank("short_term", a), "all_time": rank("long_term", a)}
                       for a in names["short_term"][:20]), key=lambda c: c["now"] - c["all_time"])
    climbers = [c for c in climbers if c["all_time"] - c["now"] >= 5][:6]
    # Fading: all-time top 15, missing from this month's top 50
    fading = [a for a in names["long_term"][:15] if a not in names["short_term"]]

    all_time = tracks["long_term"]
    years = [year(t["releaseDate"]) for t in all_time if year(t["releaseDate"])]
    decades = Counter(f"{y // 10 * 10}s" for y in years)
    now = datetime.now().year
    credits = Counter(a for t in all_time for a in t["artists"])

    hours = Counter()
    for r in recent:
        played = datetime.fromisoformat(re.sub(r"\.\d+", "", r["playedAt"]).replace("Z", "+00:00")).astimezone(CENTRAL)
        hours[played.hour] += 1

    term_stats = {}
    for term, label in TERMS.items():
        ts = tracks[term]
        term_stats[term] = {
            "label": label,
            "desi_share": round(100 * sum(map(is_desi, ts)) / len(ts)),
            "explicit_share": round(100 * sum(t["explicit"] for t in ts) / len(ts)),
            "avg_length": round(sum(t["durationMs"] for t in ts) / len(ts) / 1000),
            "median_release_year": sorted(year(t["releaseDate"]) or now for t in ts)[len(ts) // 2],
            "number_one": {"track": ts[0]["name"], "artist": ts[0]["artists"][0], "url": ts[0]["url"]},
            "ariana_share": round(100 * sum("Ariana Grande" in t["artists"] for t in ts) / len(ts)),
        }
    oldest = min(all_time, key=lambda t: t["releaseDate"])
    longest = max(all_time, key=lambda t: t["durationMs"])
    shortest = min(all_time, key=lambda t: t["durationMs"])
    song = lambda t: {"track": t["name"], "artist": t["artists"][0], "year": year(t["releaseDate"]),
                      "minutes": round(t["durationMs"] / 60000, 1), "url": t["url"]}
    return {
        "ride_or_die": ride_or_die, "climbers": climbers, "fading": fading,
        "terms": term_stats,
        "decades_all_time": dict(sorted(decades.items())),
        "avg_song_age_years": round(sum(now - y for y in years) / len(years), 1),
        "most_credited": [{"name": n, "tracks": c} for n, c in credits.most_common(8)],
        "oldest_song": song(oldest), "longest_song": song(longest), "shortest_song": song(shortest),
        "listening_clock": {str(h): hours.get(h, 0) for h in range(24)},
        "recent_minutes": round(sum(r["track"]["durationMs"] for r in recent) / 60000),
        "recent_plays": len(recent),
        "recent_unique_artists": len({r["track"]["artists"][0] for r in recent}),
    }


def watch_and_read():
    watch, read, talks = load("watch.json"), load("read.json"), load("inspiration.json")
    titles = [i for s in watch["shelves"] for i in s["items"]]
    years = [year(i["meta"]) for i in titles if year(i["meta"])]
    authors = Counter(i["meta"] for s in read["shelves"] for i in s["items"])
    speakers = Counter(t["speaker"].split(",")[0] for t in talks["talks"])
    desi = next(s for s in watch["shelves"] if "Desi" in s["title"])["items"]
    desi_count = len(desi) + sum(any(w in i["title"] for w in DESI_TITLES) for i in titles if i not in desi)
    return {
        "watch_count": len(titles),
        "watch_decades": dict(sorted(Counter(f"{y // 10 * 10}s" for y in years).items())),
        "oldest_watch": min(titles, key=lambda i: year(i["meta"]) or 9999)["title"],
        "desi_share": round(100 * desi_count / len(titles)),
        "book_count": sum(len(s["items"]) for s in read["shelves"]),
        "repeat_authors": [a for a, c in authors.items() if c > 1],
        "books_by_shelf": {s["theme"]: len(s["items"]) for s in read["shelves"]},
        "talk_count": len(talks["talks"]),
        "talks_by_topic": dict(Counter(t["topic"] for t in talks["talks"])),
        "repeat_speakers": [s for s, c in speakers.items() if c > 1],
    }


def visuals():
    """Chart-ready data for the visuals on index.html."""
    lab = load("music/music-lab.json")
    group = lambda t: "ariana" if "Ariana Grande" in t["artists"] else "desi" if is_desi(t) else "other"
    songs = {term: [{"rank": n, "track": t["name"], "artist": ", ".join(t["artists"][:2]), "art": t["albumArt"],
                     "year": year(t["releaseDate"]), "minutes": round(t["durationMs"] / 60000, 2),
                     "url": t["url"], "group": group(t)}
                    for n, t in enumerate(ts, 1)] for term, ts in lab["topTracks"].items()}

    names = {term: [a["name"] for a in lab["topArtists"][term]] for term in TERMS}
    photo = {a["name"]: a["image"] for term in TERMS for a in lab["topArtists"][term]}
    tracked = []
    for term in ("long_term", "medium_term", "short_term"):
        tracked += [a for a in names[term][:10] if a not in tracked]
    bump = [{"name": a, "image": photo[a],
             "ranks": {term: (names[term].index(a) + 1 if a in names[term] else None) for term in TERMS}}
            for a in tracked]

    recent = []
    for r in lab["recent"]:
        played = datetime.fromisoformat(re.sub(r"\.\d+", "", r["playedAt"]).replace("Z", "+00:00")).astimezone(CENTRAL)
        t = r["track"]
        recent.append({"played": played.strftime("%Y-%m-%dT%H:%M"), "track": t["name"], "artist": t["artists"][0],
                       "art": t["albumArt"], "minutes": round(t["durationMs"] / 60000, 2), "group": group(t)})

    timeline = []
    for s in load("watch.json")["shelves"]:
        for i in s["items"]:
            yrs = [int(y) for y in re.findall(r"\d{4}", i["meta"] or "")]
            if not yrs:
                continue  # stand-up specials have no year on the site
            ongoing = bool(re.search(r"\d{4}–$", i["meta"]))
            film = len(yrs) == 1 and not ongoing and i["title"] not in SINGLE_SEASON
            desi = s["title"] == "The Desi Edit" or any(w in i["title"] for w in DESI_TITLES)
            timeline.append({"title": i["title"], "shelf": s["title"], "image": i["image"], "desi": desi,
                             "start": yrs[0], "end": datetime.now().year if ongoing else yrs[-1],
                             "kind": "film" if film else "series", "ongoing": ongoing})
    timeline.sort(key=lambda x: (x["start"], x["end"]))
    return {"songs": songs, "bump": bump, "recent": recent, "watch_timeline": timeline}


def exports():
    out = os.path.join(ROOT, "exports")
    os.makedirs(out, exist_ok=True)
    rows = []
    for kind, f in [("watch", "watch.json"), ("read", "read.json")]:
        for s in load(f)["shelves"]:
            for i in s["items"]:
                rows.append({"type": kind, "shelf": s["title"], "title": i["title"], "by_or_year": i["meta"], "link": ""})
    for t in load("inspiration.json")["talks"]:
        rows.append({"type": "talk", "shelf": t["topic"], "title": t["title"], "by_or_year": t["speaker"], "link": t["youtube"]})
    for t in load("music/top-tracks.json"):
        rows.append({"type": "song", "shelf": f"Top tracks #{t['position']}", "title": t["name"], "by_or_year": t["artist"], "link": t["spotifyUrl"]})
    with open(os.path.join(out, "all-favorites.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    lab = load("music/music-lab.json")
    with open(os.path.join(out, "top-tracks-by-term.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["term", "rank", "track", "artists", "album", "release_date", "minutes", "explicit", "url"])
        for term, ts in lab["topTracks"].items():
            for n, t in enumerate(ts, 1):
                w.writerow([TERMS[term], n, t["name"], "; ".join(t["artists"]), t["album"], t["releaseDate"],
                            round(t["durationMs"] / 60000, 2), t["explicit"], t["url"]])
    return len(rows)


# Each mood comes from a caption on the website ("for sad days...", "when being a beginner feels hard").
MOODS = [
    ("Couch-potato blob day", "For sad days, lazy days, and couch-potato blob days.", [("watch", "Shows I Rewatch on Repeat")]),
    ("Hopelessly romantic", "Feeling a little delusional and in need of a happy ending.",
     [("watch", "Romance Movies That I'm In Love With"), ("read", "Books I’ll Never Shut Up About")]),
    ("Need a laugh", "Comedy that never misses.", [("watch", "Comedy That Never Misses")]),
    ("Missing home", "Bollywood, desi series, and the Hindi & Punjabi songs that keep culture in the mix.",
     [("watch", "The Desi Edit"), ("song", "desi")]),
    ("Being a beginner feels hard", "The talks I go back to when being a beginner feels hard.",
     [("talk", "Becoming"), ("read", "Books That Actually Changed How I Live")]),
    ("Want to make something", "From “wait, what if…” to something you can actually see.",
     [("talk", "Creativity"), ("read", "Books Behind the Business")]),
    ("Why do people do that?", "One innocent question becomes a 45-minute investigation.",
     [("talk", "Psychology"), ("talk", "Life & People"), ("talk", "Ideas & Brands")]),
    ("Can't stop replaying", "The songs I'm stuck on this month.", [("song", "now")]),
]


def moods():
    watch, read, talks = load("watch.json"), load("read.json"), load("inspiration.json")
    lab = load("music/music-lab.json")
    shelves = {("watch", s["title"]): s for s in watch["shelves"]}
    shelves.update({("read", s["title"]): s for s in read["shelves"]})
    out = []
    for name, why, sources in MOODS:
        picks = []
        for kind, key in sources:
            if kind in ("watch", "read"):
                picks += [{"type": kind, "title": i["title"], "by": i["meta"], "image": i["image"]}
                          for i in shelves[(kind, key)]["items"]]
            elif kind == "talk":
                picks += [{"type": "talk", "title": t["title"], "by": t["speaker"], "image": t["image"], "link": t["youtube"]}
                          for t in talks["talks"] if t["topic"] == key]
            else:
                ts = [t for t in lab["topTracks"]["long_term"] if is_desi(t)] if key == "desi" else lab["topTracks"]["short_term"][:10]
                picks += [{"type": "song", "title": t["name"], "by": ", ".join(t["artists"][:2]), "image": t["albumArt"], "link": t["url"]}
                          for t in ts]
        out.append({"mood": name, "why": why, "picks": picks})
    return out


def markdown(i):
    m, w = i["music"], i["shelves"]
    t = m["terms"]
    clock = m["listening_clock"]
    peak = max(clock, key=clock.get)
    L = ["# Insights", "",
         f"_Generated {i['generated']} by `scripts/analyze.py`. Things my website doesn't tell you._", "",
         "## Music", "",
         f"- **Ride-or-die artists** (top 15 in the last 4 weeks, 6 months *and* all time): {', '.join(m['ride_or_die']) or 'none'}",
         f"- **Climbing right now:** " + (", ".join(f"{c['name']} (#{c['all_time'] if c['all_time'] < 51 else '50+'} all time → #{c['now']} this month)" for c in m['climbers']) or "nobody new"),
         f"- **Taking a break from** (all-time top 15, missing this month): {', '.join(m['fading']) or 'none'}",
         f"- **Average song age:** {m['avg_song_age_years']} years. Oldest favorite: *{m['oldest_song']['track']}* by {m['oldest_song']['artist']} ({m['oldest_song']['year']})",
         f"- **Longest favorite:** *{m['longest_song']['track']}* ({m['longest_song']['minutes']} min). Shortest: *{m['shortest_song']['track']}* ({m['shortest_song']['minutes']} min)",
         f"- **Peak listening hour (recent plays, Austin time):** {int(peak) % 12 or 12} {'AM' if int(peak) < 12 else 'PM'}",
         f"- **Last {m['recent_plays']} plays:** {m['recent_minutes']} minutes across {m['recent_unique_artists']} artists", "",
         "| | Last 4 weeks | Last 6 months | All time |", "|---|---|---|---|"]
    for key, label in [("desi_share", "Desi songs (Bollywood, Punjabi, Indian pop)"), ("ariana_share", "Ariana Grande songs"), ("explicit_share", "Explicit"),
                       ("avg_length", "Avg length (sec)"), ("median_release_year", "Median release year")]:
        suffix = "%" if "share" in key else ""
        L.append(f"| {label} | " + " | ".join(f"{t[k][key]}{suffix}" for k in TERMS) + " |")
    L.append("| #1 track | " + " | ".join(f"{t[k]['number_one']['track']}" for k in TERMS) + " |")
    L += ["", "**Most-credited artists in my all-time top 50:** " +
          ", ".join(f"{a['name']} ({a['tracks']})" for a in m["most_credited"]), "",
          "**All-time top 50 by decade:** " + ", ".join(f"{d}: {c}" for d, c in m["decades_all_time"].items()), "",
          "## Watch, read, learn", "",
          f"- **{w['watch_count']} shows & movies**, oldest is *{w['oldest_watch']}*. By decade: " +
          ", ".join(f"{d}: {c}" for d, c in w["watch_decades"].items()),
          f"- **{w['desi_share']}%** of what I watch is Desi (Bollywood, Indian series, or desi stand-up)",
          f"- **{w['book_count']} books**: " + ", ".join(f"{k.lower()} ({v})" for k, v in w["books_by_shelf"].items()),
          f"- **Authors I came back to:** {', '.join(w['repeat_authors'])}",
          f"- **{w['talk_count']} TED talks**: " + ", ".join(f"{k} ({v})" for k, v in w["talks_by_topic"].items()),
          f"- **Speakers I watched twice:** {', '.join(w['repeat_speakers'])}", ""]
    return "\n".join(L)


def main():
    insights = {"generated": datetime.now().strftime("%Y-%m-%d"), "music": music(), "shelves": watch_and_read(),
                "visuals": visuals()}
    with open(os.path.join(ROOT, "data", "insights.json"), "w") as f:
        json.dump(insights, f, indent=2, ensure_ascii=False); f.write("\n")
    open(os.path.join(ROOT, "INSIGHTS.md"), "w").write(markdown(insights))
    with open(os.path.join(ROOT, "data", "moods.json"), "w") as f:
        json.dump(moods(), f, indent=2, ensure_ascii=False); f.write("\n")
    print("exported", exports(), "rows")


if __name__ == "__main__":
    main()
