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
    print("--User Current Playlists--")
    for playlist in user_current_playlists["items"]:
        print("Playlist's name:", playlist["name"])
        print("Playlist's ID:", playlist["id"])
        print("Playlist's description:", playlist["description"])
        print("Total tracks:", playlist["tracks"]["total"])
        print("*")
    print()
    return user_current_playlists


def view_user_saved_tracks(amount):
    user_current_saved_tracks = sp.current_user_saved_tracks()
    print("--User Current Saved Tracks--")
    print(f"First {amount} current saved tracks")
    for i in range(len(user_current_saved_tracks["items"][:amount])):
        current_track = user_current_saved_tracks["items"][i]["track"]
        print("Track's name:", current_track["name"])
        print("Track's album:", current_track["album"]["name"])
        print("Track's artist:", current_track["artists"][0]["name"])
        print("*")
    print()
    return user_current_saved_tracks


def view_weekly_discovery_tracks():
    weekly_playlist_url = "https://open.spotify.com/playlist/37i9dQZEVXcSl5JcFboUlo?si=105e91e417bc41a0"
    weekly_playlist = sp.playlist(playlist_id=weekly_playlist_url)
    print("---Discover Weekly Tracks---")
    for track in weekly_playlist["tracks"]["items"]:
        print("Track's name:", track["track"]["name"])
        print("Artist:", track["track"]["artists"][0]["name"])
        print("Track's ID:", track["track"]["id"])
        print("*")
    print()
    return weekly_playlist


def view_day_list_tracks():
    day_list_url = "https://open.spotify.com/playlist/37i9dQZF1EP6YuccBxUcC1?si=e772f4d4e4c547f4"
    day_list_playlist = sp.playlist(playlist_id=day_list_url)
    print("---Current Day List Tracks---")
    for track in day_list_playlist["tracks"]["items"]:
        track_info = track["track"]
        print("Name:", track_info["name"])
        print("Artist:", track_info["artists"][0]["name"])
        print("Album:", track_info["album"]["name"])
        print("*")
    print()
    return day_list_playlist


def create_playlist(name, description=""):
    user = sp.current_user()
    # Make sure there's no duplicated playlist name
    user_playlists = sp.current_user_playlists()
    for playlist in user_playlists["items"]:
        if playlist["name"] == name:
            print("Playlist name already exists. Please choose another one")
            return
    new_playlist = sp.user_playlist_create(user=user["id"], name=name, public=True, collaborative=False, description=description)
    print(f"Playlist {name} has been created")
    return new_playlist


def add_songs_to_playlist(playlist_id, items):
    playlist = sp.playlist_add_items(playlist_id=playlist_id, items=items)
    print("Songs have been added to the playlist.")
    return playlist


def add_songs_from_daylist_playlist(playlist_id):
    daylist_url = "https://open.spotify.com/playlist/37i9dQZF1EP6YuccBxUcC1?si=f5d4859eafbd461c"
    daylist_tracks = sp.playlist_items(playlist_id=daylist_url)

    # Get Day List's tracks' ID
    tracks_id = []
    for track in daylist_tracks["items"]:
        tracks_id.append(track["track"]["id"])

    # Add Day List's tracks to the given playlist
    playlist = sp.playlist_add_items(playlist_id=playlist_id, items=tracks_id)
    print("All songs from current Day List Playlist have been added.")
    return playlist


def add_songs_from_weekly_playlist(playlist_id):
    weekly_url = "https://open.spotify.com/playlist/37i9dQZEVXcSl5JcFboUlo"
    weekly_tracks = sp.playlist_items(playlist_id=weekly_url)

    # Get Discover Weekly's tracks' ID
    tracks_id = []
    for track in weekly_tracks["items"]:
        tracks_id.append(track["track"]["id"])

    # Add Discover Weekly's tracks to the give playlist
    playlist = sp.playlist_add_items(playlist_id=playlist_id, items=tracks_id)
    print("All songs from this week Discover Weekly Playlist have been added.")
    return playlist


def view_playlist_tracks(playlist_id):
    playlist_tracks = sp.playlist_items(playlist_id=playlist_id)
    for tracks in playlist_tracks["items"]:
        track = tracks["track"]
        print("Name:", track["name"])
        print("Album:", track["album"]["name"])
        print("Artist:", track["artists"][0]["name"])
        print("*")
    return playlist_tracks