import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_secrets import CLIENT_ID, CLIENT_SECRET


os.environ["SPOTIPY_CLIENT_ID"] = CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:9000"
scope = "user-library-read user-library-modify playlist-modify-public"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
print("---User Info---")
user = sp.current_user()
user_id = user["id"]
print("User's ID:", user_id)
print("User's name:", user["display_name"])
print("User's followers:", user["followers"]["total"])


print("---User Playlist---")
# user_playlists = sp.user_playlists(user=user_id, limit=10)
current_user_playlists = sp.current_user_playlists(limit=10)
print(current_user_playlists["items"][0].keys())
for p in current_user_playlists["items"]:
    print("Playlist's name:", p["name"])
    print("Playlist's owner:", p["owner"]["display_name"])
    print()


print("---Discover Weekly Playlist---")
weekly_discovery_playlist_url = "https://open.spotify.com/playlist/37i9dQZEVXcSl5JcFboUlo?si=c1f8e1d45057476e"
discover_weekly_playlist = sp.playlist(weekly_discovery_playlist_url)
# print(discover_weekly_playlist["tracks"]["items"])
# print(len(discover_weekly_playlist["tracks"]["items"]))
for track in discover_weekly_playlist["tracks"]["items"]:
    # print(track["track"].keys())
    print("Track's name:", track["track"]["name"])
    print("Artist:", track["track"]["artists"][0]["name"])
    print("Track's ID:", track["track"]["id"])
    print("*")


print("---Add songs---")
# added_songs = sp.playlist_add_items(playlist_id="https://open.spotify.com/playlist/47pIp4za3M5vRfcEqCuhJy?si=fde989dc0dd040dc", items=["https://open.spotify.com/track/5dn6QANKbf76pANGjMBida?si=734b709192c84050"])
print("Songs have been added.")

print("---Daylist Tracks---")
daylist_url = "https://open.spotify.com/playlist/37i9dQZF1EP6YuccBxUcC1?si=f5d4859eafbd461c"
daylist_tracks = sp.playlist_items(playlist_id=daylist_url)
print(daylist_tracks["total"])
for item in daylist_tracks["items"]:
    # print(item.keys())
    track = item["track"]
    print(item["track"].keys())
    print("Name:", track["name"])
    print("Artist:", track["artists"][0]["name"])
    print("Album:", track["album"]["name"])
    print("ID", track["id"])
    print("*")


# Create playlist
playlists = sp.current_user_playlists()
new_playlist = {}
found = False
print(type(playlists))
print(playlists.keys())
for playlist in playlists["items"]:
    print(playlist["name"])
    if playlist["name"] == "New playlist":
        found = True
        break

if not found:
    new_playlist = sp.user_playlist_create(user=user_id, name=f"New playlist", public=True, collaborative=False,
                                           description="Created by Spotipy.")
print(new_playlist)



