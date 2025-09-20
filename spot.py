#!/usr/bin/env python3
import os
import sys
import re
import csv
from pathlib import Path
import argparse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List, Dict

# --- Auth ---
os.environ["SPOTIPY_REDIRECT_URI"] = "http://127.0.0.1:8888/callback/"
scope = [
    "user-library-read",
    "user-library-modify",
    "playlist-modify-public",
    "playlist-read-private",
    "playlist-modify-private",
]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

CACHE_FILE = Path.home() / ".spotify/playlists"

# --- Utilities ---
def print_tsv(rows: List[Dict[str, str]], headers: List[str]):
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(row.get(h, "")) for h in headers))

def parse_stdin_table() -> List[Dict[str, str]]:
    lines = [l.strip() for l in sys.stdin if l.strip()]
    if not lines:
        return []
    headers = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        values = line.split("\t")
        rows.append(dict(zip(headers, values)))
    return rows

def parse_song_arg(song: str) -> Dict[str, str]:
    if song.startswith("spotify:track:") or "open.spotify.com/track/" in song:
        return {"url": song}
    if song == "-":
        return {"url": "-"}
    if " - " in song:
        artist, title = song.split(" - ", 1)
        return {"artist": artist.strip(), "title": title.strip()}
    return {"artist": "", "title": song.strip()}

# --- Playlist resolution & caching ---
def is_playlist_id(ref: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9]{22}", ref))

def is_playlist_url(ref: str) -> bool:
    return ref.startswith("https://open.spotify.com/playlist/")

def is_playlist_uri(ref: str) -> bool:
    return ref.startswith("spotify:playlist:")

def save_playlist_cache(playlists: List[Dict[str,str]]):
    # Ensure parent directory exists
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id","name","url"], delimiter="\t")
        writer.writeheader()
        writer.writerows(playlists)

def fetch_user_playlists() -> Dict[str,str]:
    playlists = []
    lookup = {}
    results = sp.current_user_playlists()
    while results:
        for pl in results["items"]:
            playlists.append({"id": pl["id"], "name": pl["name"], "url": pl["external_urls"]["spotify"]})
            lookup[pl["name"]] = pl["id"]
        if results.get("next"):
            results = sp.next(results)
        else:
            results = None
    save_playlist_cache(playlists)
    return lookup

def load_playlist_cache() -> Dict[str,str]:
    if not CACHE_FILE.exists():
        return fetch_user_playlists()
    try:
        lookup = {}
        with open(CACHE_FILE, newline="") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                lookup[row["name"]] = row["id"]
        return lookup
    except Exception:
        return fetch_user_playlists()

def resolve_playlist_ref(ref: str) -> str:
    if is_playlist_id(ref):
        return ref
    if is_playlist_url(ref):
        return ref.split("/")[-1].split("?")[0]
    if is_playlist_uri(ref):
        return ref.split(":")[-1]
    # treat as name
    lookup = load_playlist_cache()
    if ref in lookup:
        return lookup[ref]
    lookup = fetch_user_playlists()
    if ref in lookup:
        return lookup[ref]
    raise ValueError(f"Playlist '{ref}' not found in cache or Spotify account")

def search_track(artist: str, title: str) -> str:
    query = f"track:{title} artist:{artist}"
    results = sp.search(q=query, type="track", limit=1)
    items = results.get("tracks", {}).get("items", [])
    if items:
        return items[0]["external_urls"]["spotify"]
    return ""

# --- Commands ---
def cmd_user_info(_args):
    user = sp.current_user()
    rows = [{"id": user["id"], "name": user.get("display_name",""), "followers": user["followers"]["total"]}]
    print_tsv(rows, ["id","name","followers"])

def cmd_playlists_list(_args):
    lookup = fetch_user_playlists()
    rows = [{"id": pid, "name": name, "url": f"https://open.spotify.com/playlist/{pid}"} for name,pid in lookup.items()]
    print_tsv(rows, ["id","name","url"])

def cmd_playlists_create(args):
    user = sp.current_user()
    # Load current playlists (cache or fetch)
    current_playlists = load_playlist_cache()
    if args.name in current_playlists:
        print(f"Playlist '{args.name}' already exists. Choose a different name.", file=sys.stderr)
        return

    new_pl = sp.user_playlist_create(
        user=user["id"],
        name=args.name,
        public=not args.private,
        description=args.description or ""
    )

    # Update cache
    current_playlists[new_pl["name"]] = new_pl["id"]
    save_playlist_cache([
        {"id": pid, "name": name, "url": f"https://open.spotify.com/playlist/{pid}"}
        for name, pid in current_playlists.items()
    ])

    # Output created playlist
    rows = [{"id": new_pl["id"], "name": new_pl["name"], "url": new_pl["external_urls"]["spotify"]}]
    print_tsv(rows, ["id", "name", "url"])

def cmd_playlists_tracks(args):
    playlist_id = resolve_playlist_ref(args.playlist)
    items = sp.playlist_items(playlist_id=playlist_id)
    rows = []
    for t in items["items"]:
        track = t["track"]
        rows.append({"artist": track["artists"][0]["name"], "title": track["name"], "url": track["external_urls"]["spotify"]})
    print_tsv(rows, ["artist","title","url"])

def cmd_playlists_add(args):
    playlist_id = resolve_playlist_ref(args.playlist)
    track_urls = []
    for song in args.songs:
        parsed = parse_song_arg(song)
        if parsed.get("url") == "-":
            rows = parse_stdin_table()
            for r in rows:
                url = r.get("url","").strip()
                if url: track_urls.append(url)
        elif parsed.get("url"):
            track_urls.append(parsed["url"])
        else:
            url = search_track(parsed["artist"], parsed["title"])
            if url: track_urls.append(url)
    if track_urls:
        sp.playlist_add_items(playlist_id, track_urls)
        print_tsv([{"url": u} for u in track_urls], ["url"])

def cmd_playlists_remove(args):
    playlist_id = resolve_playlist_ref(args.playlist)
    track_urls = []
    for song in args.songs:
        parsed = parse_song_arg(song)
        if parsed.get("url") == "-":
            rows = parse_stdin_table()
            for r in rows:
                url = r.get("url","").strip()
                if url: track_urls.append(url)
        elif parsed.get("url"):
            track_urls.append(parsed["url"])
        else:
            url = search_track(parsed["artist"], parsed["title"])
            if url: track_urls.append(url)
    if track_urls:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, track_urls)
        print_tsv([{"url": u} for u in track_urls], ["url"])

def cmd_search(args):
    track_urls = []
    for song in args.songs:
        parsed = parse_song_arg(song)
        if parsed.get("url") == "-":
            rows = parse_stdin_table()
            for r in rows:
                artist = r.get("artist","")
                title = r.get("title","")
                if title:
                    url = search_track(artist,title)
                    if url: track_urls.append({"url":url})
        elif parsed.get("url"):
            track_urls.append({"url": parsed["url"]})
        else:
            url = search_track(parsed["artist"], parsed["title"])
            if url: track_urls.append({"url":url})
    print_tsv(track_urls, ["url"])

# --- CLI Parser ---
def main():
    parser = argparse.ArgumentParser(prog="spotify-cli")
    subparsers = parser.add_subparsers(dest="command")

    # user
    user_parser = subparsers.add_parser("user")
    user_sub = user_parser.add_subparsers(dest="subcommand")
    user_sub.add_parser("info").set_defaults(func=cmd_user_info)

    # playlists
    pl_parser = subparsers.add_parser("playlists")
    pl_sub = pl_parser.add_subparsers(dest="subcommand")
    pl_sub.add_parser("list").set_defaults(func=cmd_playlists_list)
    create_parser = pl_sub.add_parser("create")
    create_parser.add_argument("name")
    create_parser.add_argument("--description")
    create_parser.add_argument("--private", action="store_true")
    create_parser.set_defaults(func=cmd_playlists_create)
    tracks_parser = pl_sub.add_parser("tracks")
    tracks_parser.add_argument("playlist")
    tracks_parser.set_defaults(func=cmd_playlists_tracks)
    add_parser = pl_sub.add_parser("add")
    add_parser.add_argument("playlist")
    add_parser.add_argument("songs", nargs="+")
    add_parser.set_defaults(func=cmd_playlists_add)
    remove_parser = pl_sub.add_parser("remove")
    remove_parser.add_argument("playlist")
    remove_parser.add_argument("songs", nargs="+")
    remove_parser.set_defaults(func=cmd_playlists_remove)

    # search
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("songs", nargs="+")
    search_parser.set_defaults(func=cmd_search)

    args = parser.parse_args()
    if not args.command or not hasattr(args,"func"):
        parser.print_help()
        sys.exit(1)
    args.func(args)

if __name__ == "__main__":
    main()
