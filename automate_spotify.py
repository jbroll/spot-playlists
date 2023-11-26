import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = "7777ac4f09a747a1ab0f0e1cef7a2323"
CLIENT_SECRET = "11cf4026d8084e4ca99081bb8c2f93cd"

# Set up Authorization
os.environ["SPOTIPY_CLIENT_ID"] = CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:9000"
scope = ["user-library-read user-library-modify playlist-modify-public"]

# Set up spotipy.client.Spotify object which is authenticated
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def view_user_info():
    user = sp.current_user()
    print("--User Info--")
    print("Name:", user["display_name"])
    print("Total followers:", user["followers"]["total"])
    print()
    return user


def view_user_playlists():
    user_current_playlists = sp.current_user_playlists()
    print("--User Current Playlists---")
    for playlist in user_current_playlists["items"]:
        print("Playlist's name:", playlist["name"])
        print("Playlist's ID:", playlist["id"])
        print("Playlist's description:", playlist["description"])
        print("Total tracks:", playlist["tracks"]["total"])
        print("*")
    print()


def view_user_saved_tracks(amount=10):
    user_current_saved_tracks = sp.current_user_saved_tracks(limit=10)
    print("--User Current Saved Tracks--")
    print(f"First {amount} current saved tracks")
    for i in range(len(user_current_saved_tracks["items"][:amount])):
        current_track = user_current_saved_tracks["items"][i]["track"]
        print("Track's name:", current_track["name"])
        print("Track's album:", current_track["album"]["name"])
        print("Track's artist:", current_track["artists"][0]["name"])
        print("*")
    print()


def view_weekly_discovery_tracks():
    weekly_playlist_url = "https://open.spotify.com/playlist/37i9dQZEVXcSl5JcFboUlo?si=105e91e417bc41a0"
    weekly_playlist = sp.playlist(playlist_id=weekly_playlist_url)

    for track in weekly_playlist["tracks"]["items"]:
        track_info = track["track"]
        print("Name:", track_info["name"])
        print("Artist:", track_info["artists"][0]["name"])
        print("Album:", track_info["album"]["name"])
        print("*")
    print()