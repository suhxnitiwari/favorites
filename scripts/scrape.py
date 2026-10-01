"""Rebuild data/ and images/ from https://suhanitiwari.com/home/favorites.

Usage: python3 scripts/scrape.py
"""
import html, json, os, re, urllib.request

SITE = "https://suhanitiwari.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


def fetch(path):
    req = urllib.request.Request(SITE + path, headers={"User-Agent": "favorites-scraper"})
    return urllib.request.urlopen(req, timeout=60).read()


def text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip() or None


def grab(pattern, s):
    m = re.search(pattern, s, re.S)
    return text(m.group(1)) if m else None


def download(src):
    """Save a site image under images/ and return its repo-relative path."""
    rel = src.lstrip("/")
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            with open(path, "wb") as f:
                f.write(fetch(src))
        except Exception as e:
            print("skipped image", src, e)
            return None
    return rel


def image_of(s):
    m = re.search(r'<img src="([^"]+)"', s)
    return download(m.group(1)) if m else None


def parse_shelves(chunk):
    shelves = []
    # A "fav-q" line ("01 How things work") labels the shelf that follows it.
    parts = re.split(r'(<p class="fav-q">.*?</p>|<div class="shelf[ "][^>]*>)', chunk, flags=re.S)
    eyebrow = None
    for i, part in enumerate(parts):
        if part.startswith('<p class="fav-q">'):
            eyebrow = text(re.sub(r"<b>.*?</b>", "", part))
        elif part.startswith('<div class="shelf') and "video-shelf" not in part:
            block = parts[i + 1]
            items = [{"title": grab(r'shelf-item-title">(.*?)</p>', li),
                      "meta": grab(r'shelf-item-meta">(.*?)</p>', li),
                      "image": image_of(li)}
                     for li in re.findall(r'<li class="shelf-item">(.*?)</li>', block, re.S)]
            shelves.append({"title": grab(r'class="shelf-title">(.*?)</h3>', block),
                            "theme": eyebrow,
                            "caption": grab(r'shelf-caption">(.*?)</p>', block),
                            "items": items})
            eyebrow = None
    return shelves


def parse_talks(page):
    why = dict((text(t), text(b)) for t, b in re.findall(
        r'class="why-topic">(.*?)</span>\s*<p class="why-text">(.*?)</p>', page, re.S))
    talks = []
    for topic, li in re.findall(r'<li class="shelf-item" data-topic="([^"]*)">(.*?)</li>', page, re.S):
        vid = re.search(r'data-video="([^"]+)"', li).group(1)
        talks.append({"topic": html.unescape(topic),
                      "title": grab(r'shelf-item-title">(.*?)</span>', li),
                      "speaker": grab(r'shelf-item-meta">(.*?)</span>', li),
                      "youtube": f"https://www.youtube.com/watch?v={vid}",
                      "image": image_of(li)})
    return {"tagline": "Some people have comfort shows. I have comfort TED talks.",
            "why_i_watch": why, "talks": talks}


def write(name, obj):
    with open(os.path.join(DATA, name), "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    page = fetch("/home/favorites").decode()
    watch_at, read_at = page.find('id="watch"'), page.find('id="read"')
    type_at = page.find('class="fav-type"')
    claim = lambda s: (lambda m: {"headline": text(m.group(1)), "body": text(m.group(2))} if m else None)(
        re.search(r'class="fav-claim"><strong>(.*?)</strong>(.*?)</p>', s, re.S))

    takeaway = re.search(r'<aside class="fav-takeaway">(.*?)</aside>', page, re.S).group(1)
    paras = [text(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", takeaway, re.S)]
    write("listen.json", {"intro": "I listen by feeling, not by genre.",
                          "claim": {"headline": paras[1], "body": paras[2]}})

    talks_at = page.find('data-topic=')
    write("watch.json", {"claim": claim(page[watch_at:read_at]),
                         "shelves": parse_shelves(page[watch_at:talks_at])
                                    + parse_shelves(page[page.find('id="watchMore"'):read_at])})
    write("inspiration.json", parse_talks(page[watch_at:read_at]))
    write("read.json", {"claim": claim(page[read_at:]),
                        "shelves": parse_shelves(page[read_at:type_at])})

    grid = page[type_at:]
    write("my-type.json", {
        "headline": grab(r'<h2[^>]*>(.*?)</h2>', grid),
        "subhead": grab(r'fav-type-sub">(.*?)</p>', grid),
        "themes": [{"name": text(n), "from": text(f), "why": text(w)} for n, f, w in re.findall(
            r'<h3>(.*?)</h3>\s*<p class="fav-type-from">(.*?)</p>\s*<p>(.*?)</p>', grid, re.S)]})

    for endpoint, out in [("GetTopTracks?limit=50", "top-tracks"), ("GetTopArtists?limit=20", "top-artists"),
                          ("GetTopGenres?limit=5", "top-genres"), ("GetRecentlyPlayed", "recently-played"),
                          ("GetMusicLab", "music-lab")]:
        data = json.loads(fetch("/spotify/" + endpoint))
        if out == "music-lab":
            # keep the listening history, drop account/device details
            data = {k: data[k] for k in ("topTracks", "topArtists", "recent") if k in data}
        write(f"music/{out}.json", data)


if __name__ == "__main__":
    main()
