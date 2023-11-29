# Spotify Playlist Manager

## Introduction
This project is a Python CLI (Command Line Interface) tool designed to interact with Spotipy's API using the Spotipy library. It allows users to view their playlists, saved tracks, create new playlists, and add songs to existing playlists.


## Technology:
- Backend: Python, Argparse library, Spotipy library.
- Task scheduler: Crontab.


## Features
- View Playlist and Saved Tracks: Easily access your Spotify playlists and saved tracks with details.
- Create Playlists: Create new playlists directly from the commandline.
- Add songs to Playlist: Add songs to your existing playlists with simple commands.
- Automated Playlist updates:
  - Every 3 hours, songs from user's **_Day List_** playlist are automatically added to a user-specified playlist.
  - Every Monday, songs from user's Discover Weekly playlist are added to another user-specified playlist.
- Task Scheduling: Utilizes "crontab" for scheduling tasks like playlist updates. 
- Find my playlist automated by this tool at <a href="https://open.spotify.com/playlist/67fRWrYNLNRQ4Z0az53tVH?si=deb261ee8dda4dd4">here</a>

## Getting Started

### Prerequisites
- Python 3.11.0
- Access to Spotify's API (requires Spotify developer account)

### Installation
- Clone the repository
```commandline
git clone https://github.com/quynhnle135/automate-spotify-playlist.git
```

- Install required packages
```commandline
pip install -r requirements.txt
```

### Configuration
- Create Spotify's App at: https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app
- Get your CLIENT_ID and CLIENT_SECRET and update them in ```automate_spotify.py```


```python
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"

# Set up Authorization
os.environ["SPOTIPY_CLIENT_ID"] = CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:9000"
scope = ["user-library-read user-library-modify playlist-modify-public"]

# Set up spotipy.client.Spotify object which is authenticated
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
```

## Usage
```commandline
A Python CLI tool for managing Spotify playlists and tracks.

options:
  -h, --help            show this help message and exit
  -u, --user            Display the user's Spotify profile information.
  -p, --playlists       List all playlists in the user's Spotify account.
  -t TRACKS, --tracks TRACKS
                        Display a specified number of saved tracks from the user's account.
  -w, --weekly          Show the user's Discover Weekly playlist curated by Spotify.
  -d, --daylist         Show the user's current Day List Playlist curated by Spotify.
  -c CREATE, --create CREATE
                        Create a new playlist. Playlist's name is required and description is optional.
  -a ADD, --add ADD     Add songs to an existing playlist. Enter playlist's URL.
  -ad ADDDAYLIST, --adddaylist ADDDAYLIST
                        Add tracks from Day List to a specified playlist. Enter playlist's URL.
  -aw ADDWEEKLY, --addweekly ADDWEEKLY
                        Add tracks from Discover Weekly to a specified playlist. Enter playlist's URL.
  -vp VIEWPLAYLIST, --viewplaylist VIEWPLAYLIST
                        Display all tracks from the given playlist.
  -de DESCRIPTION, --description DESCRIPTION
                        Set a description for a new playlist being created.
  -so SONGS [SONGS ...], --songs SONGS [SONGS ...]
                        Add a list of songs URLs to a specified playlist.

```

### Spotify Playlist Management CLI Tool in Action

- Display User's Information

![spotify-2.png](screenshots%2Fspotify-2.png)

- Display User's Playlists

![spotify-3.png](screenshots%2Fspotify-3.png)

- Display User's 5 current saved tracks

![spotify-4.png](screenshots%2Fspotify-4.png)

- Display all tracks from User's Discover Weekly playlist (curated by Spotify)

![spotify-5.png](screenshots%2Fspotify-5.png)

- Display all tracks from User's Day List playlist (curated by Spotify)

![spotify-6.png](screenshots%2Fspotify-6.png)

- Create new playlist

![spotify-7.png](screenshots%2Fspotify-7.png)

- Here's the empty playlist created from the above command line

![spotify-8-playlist.png](screenshots%2Fspotify-8-playlist.png)

- Add songs from Day List playlist to the playlist I've just created.

![spotify-9.png](screenshots%2Fspotify-9.png)

- Here's what the playlist looks like after addings songs from Day List

![spotify-9-playlist.png](screenshots%2Fspotify-9-playlist.png)

- Here's the playlist automated by this Spotify Playlist Management CLI took with scheduled task using Crontab, which is updated with songs from Day List every 3 hours.

![spotify-result.png](screenshots%2Fspotify-result.png)
