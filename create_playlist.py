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
user = sp.current_user()
user_id = user["id"]

# Get all songs from Discovery Weekly
weekly_playlist_url = "https://open.spotify.com/playlist/37i9dQZEVXcSl5JcFboUlo?si=105e91e417bc41a0"
weekly_playlist = sp.playlist(playlist_id=weekly_playlist_url)
print(weekly_playlist.keys())
print(weekly_playlist["tracks"].keys())
print(weekly_playlist["tracks"]["items"][0])
all_weekly_playlist_tracks = []

for track in weekly_playlist["tracks"]["items"]:
    track_info = track["track"]
    print("Name:", track_info["name"])
    print("Artist:", track_info["artists"][0]["name"])
    print("Album:", track_info["album"]["name"])
    print("ID:", track_info["id"])
    all_weekly_playlist_tracks.append(track_info["id"])
    print("*")

print(all_weekly_playlist_tracks)
print(len(all_weekly_playlist_tracks))

# Create playlist
new_playlist = sp.user_playlist_create(user=user_id, name=f"New playlist", public=True, collaborative=False, description="Created by Spotipy.")

# Add songs to the new playlist
add_songs = sp.playlist_add_items(playlist_id=new_playlist["id"], items=all_weekly_playlist_tracks)



