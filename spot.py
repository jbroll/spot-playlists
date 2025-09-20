#!/usr/bin/env python3
import os
import sys
import csv
import re
from pathlib import Path
import argparse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List, Dict

# ------------------ Auth ------------------
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

# ------------------ Utilities ------------------
def print_tsv(rows: List[Dict[str, str]], headers: List[str]):
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(row.get(h, "")) for h in headers))

def parse_stdin_table() -> List[Dict[str, str]]:
    lines = [l.rstrip("\n") for l in sys.stdin if l.strip()]
    if not lines:
        raise ValueError("No input received on stdin for '-' song argument")
    headers = [h.strip().lower() for h in lines[0].split("\t")]
    rows = []
    for line in lines[1:]:
        values = line.split("\t")
        if len(values) != len(headers):
            raise ValueError(f"Invalid row: {line}")
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

def normalize_songs_arg(songs: List[str]) -> List[Dict[str,str]]:
    rows = []
    if songs == ["-"]:
        table = parse_stdin_table()
        if not table:
            return []
        headers = [h.lower() for h in table[0].keys()]
        if headers == ["url"]:
            for r in table:
                rows.append({"url": r["url"].strip()})
        elif headers == ["artist","title"]:
            for r in table:
                rows.append({"artist": r["artist"].strip(), "title": r["title"].strip()})
        else:
            raise ValueError(f"Unexpected stdin table headers: {headers}")
    else:
        for s in songs:
            rows.append(parse_song_arg(s))
    return rows

# ------------------ Playlist Cache ------------------
def is_playlist_id(ref: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9]{22}", ref))

def is_playlist_url(ref: str) -> bool:
    return ref.startswith("https://open.spotify.com/playlist/")

def is_playlist_uri(ref: str) -> bool:
    return ref.startswith("spotify:playlist:")

def save_playlist_cache(playlists: List[Dict[str,str]]):
    if CACHE_FILE.parent.exists():
        if not CACHE_FILE.parent.is_dir():
            raise RuntimeError(f"{CACHE_FILE.parent} exists but is not a directory")
    else:
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

# ------------------ Commands ------------------
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
    current_playlists[new_pl["name"]] = new_pl["id"]
    save_playlist_cache([
        {"id": pid, "name": name, "url": f"https://open.spotify.com/playlist/{pid}"}
        for name, pid in current_playlists.items()
    ])
    rows = [{"id": new_pl["id"], "name": new_pl["name"], "url": new_pl["external_urls"]["spotify"]}]
    print_tsv(rows, ["id","name","url"])

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
    track_rows = normalize_songs_arg(args.songs)
    track_urls = []
    for row in track_rows:
        if row.get("url") and row["url"] != "-":
            track_urls.append(row["url"])
        else:
            url = search_track(row["artist"], row["title"])
            if url:
                track_urls.append(url)
    if track_urls:
        sp.playlist_add_items(playlist_id, track_urls)
        print_tsv([{"url": u} for u in track_urls], ["url"])

def cmd_playlists_remove(args):
    playlist_id = resolve_playlist_ref(args.playlist)
    track_rows = normalize_songs_arg(args.songs)
    track_urls = []
    for row in track_rows:
        if row.get("url") and row["url"] != "-":
            track_urls.append(row["url"])
        else:
            url = search_track(row["artist"], row["title"])
            if url:
                track_urls.append(url)
    if track_urls:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, track_urls)
        print_tsv([{"url": u} for u in track_urls], ["url"])

def cmd_search(args):
    track_rows = normalize_songs_arg(args.songs)
    results = []
    for row in track_rows:
        if row.get("url") and row["url"] != "-":
            results.append({"url": row["url"]})
        else:
            url = search_track(row["artist"], row["title"])
            if url:
                results.append({"url": url})
    print_tsv(results, ["url"])

# ------------------ CLI Parser ------------------
def main():
    parser = argparse.ArgumentParser(prog="spotify-cli")
    parser.set_defaults(func=lambda args: parser.print_help())
    subparsers = parser.add_subparsers(dest="command", required=True)

    # user
    user_parser = subparsers.add_parser("user", help="User information commands")
    user_parser.set_defaults(func=lambda args: user_parser.print_help())
    user_sub = user_parser.add_subparsers(dest="subcommand", required=True)
    user_sub.add_parser("info", help="Show current user info").set_defaults(func=cmd_user_info)

    # playlists
    pl_parser = subparsers.add_parser("playlists", help="Playlist management commands")
    pl_parser.set_defaults(func=lambda args: pl_parser.print_help())
    pl_sub = pl_parser.add_subparsers(dest="subcommand", required=True)
    pl_sub.add_parser("list", help="List all playlists").set_defaults(func=cmd_playlists_list)

    create_p = pl_sub.add_parser("create", help="Create a playlist")
    create_p.add_argument("name", help="Name of the new playlist")
    create_p.add_argument("-d","--description", help="Playlist description")
    create_p.add_argument("-p","--private", action="store_true", help="Create as private playlist")
    create_p.set_defaults(func=cmd_playlists_create)

    tracks_p = pl_sub.add_parser("tracks", help="Show tracks in a playlist")
    tracks_p.add_argument("playlist", help="Playlist name or ID or URL")
    tracks_p.set_defaults(func=cmd_playlists_tracks)

    add_p = pl_sub.add_parser("add", help="Add tracks to a playlist")
    add_p.add_argument("playlist", help="Playlist name or ID or URL")
    add_p.add_argument("songs", nargs="+", help="Tracks to add, or '-' for stdin table")
    add_p.set_defaults(func=cmd_playlists_add)

    remove_p = pl_sub.add_parser("remove", help="Remove tracks from a playlist")
    remove_p.add_argument("playlist", help="Playlist name or ID or URL")
    remove_p.add_argument("songs", nargs="+", help="Tracks to remove, or '-' for stdin table")
    remove_p.set_defaults(func=cmd_playlists_remove)

    # search
    search_p = subparsers.add_parser("search", help="Search tracks by artist/title")
    search_p.add_argument("songs", nargs="+", help="Tracks to search, or '-' for stdin table")
    search_p.set_defaults(func=cmd_search)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
