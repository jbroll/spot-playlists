from automate_spotify import *


# View user's info
user = view_user_info()
print("view_user_info's return value DATA TYPE:", type(user))

# View user's playlists
user_playlists = view_user_playlists()
print("view_user_playlists's return value DATA TYPE:", type(user_playlists))

# View user's saved tracks
user_saved_tracks = view_user_saved_tracks(amount=5)
print("view_user_saved_tracks's return value DATA TYPE", type(user_saved_tracks))

# View user's Weekly Discovery tracks
user_weekly_discovery_tracks = view_weekly_discovery_tracks()
print("view_weekly_discovery_tracks's return value DATA TYPE:", type(user_weekly_discovery_tracks))

# View user's Daylist tracks
user_daylist_tracks = view_day_list_tracks()
print("view_day_list_tracks's return value DATA TYPE:", type(user_daylist_tracks))

# View specific playlist's tracks
playlist_id = "https://open.spotify.com/playlist/5VGiTqfGQ4B2ZmSUjLlsIk?si=fac61d5843804233"
buon_hay_vui_playlist_tracks = view_playlist_tracks(playlist_id=playlist_id)
print("view_playlist_tracks's return value DATA TYPE:", type(buon_hay_vui_playlist_tracks))

# View create_playlist's return value DATA TYPE
newest_playlist = create_playlist(name="New Playlist 20240104", description="Created from Quinn's Spotify Playlist Manager project")
print("create_playlist's return value DATA TYPE:", type(newest_playlist))

# View add_songs_to_playlist's return value DATA TYPE
newest_playlist_id = "https://open.spotify.com/playlist/20BIsq6TjlrtRKW7hBHD3t?si=e289c8ca2343403e"
items = ["https://open.spotify.com/track/1gugDOSMREb34Xo0c1PlxM?si=32c3068871ed4844", "https://open.spotify.com/track/556IN8IgPqZORjhmlyAXaP?si=2d4f147708ab4d47", "https://open.spotify.com/track/556IN8IgPqZORjhmlyAXaP?si=3696568a7ea64428"]
newest_playlist = add_songs_to_playlist(playlist_id=newest_playlist_id, items=items)
print("add_songs_to_playlist's return value DATA TYPE:", type(newest_playlist))

