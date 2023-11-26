# import os
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
#
#
# CLIENT_ID = "7777ac4f09a747a1ab0f0e1cef7a2323"
# CLIENT_SECRET = "11cf4026d8084e4ca99081bb8c2f93cd"
#
# # Set up Authorization
# os.environ["SPOTIPY_CLIENT_ID"] = CLIENT_ID
# os.environ["SPOTIPY_CLIENT_SECRET"] = CLIENT_SECRET
# os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:9000"
# scope = ["user-library-read user-library-modify playlist-modify-public"]
#
# # Set up spotipy.client.Spotify object which is authenticated
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
