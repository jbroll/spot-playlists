# Spotify Playlist Manager

## Introduction
This project is a Python CLI (Command Line Interface) tool designed to interact
with Spotify's API using the Spotipy library. It allows users to view their
playlists, saved tracks, create new playlists, and add songs to existing
playlists.

## Technology
- Backend: Python, Argparse library, Spotipy library.
- Task scheduler: Crontab (optional).

## Features
- View Playlist and Saved Tracks: Easily access your Spotify playlists and saved tracks with details.
- Create Playlists: Create new playlists directly from the command line.
- Add Songs to Playlist: Add songs to your existing playlists with simple commands.
- Automated Playlist Updates:
  - Every 3 hours, songs from the user's **Day List** playlist can be automatically added to a user-specified playlist.
  - Every Monday, songs from the user's Discover Weekly playlist can be added to another user-specified playlist.
- Task Scheduling: Utilizes "crontab" for scheduling tasks like playlist updates.

## Getting Started

### Prerequisites
- Python 3.11 or newer
- Access to Spotify's API (requires a Spotify developer account)

### Installation
1. Clone the repository:

   ```bash
   git clone https://github.com/quynhnle135/automate-spotify-playlist.git
   ```

2. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration
1. Create a Spotify App at: [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Obtain your `CLIENT_ID` and `CLIENT_SECRET`.
3. Place these values in a shell-format file at `~/.spotify/spotify-auth`:

   ```bash
   $ cat ~/.spotify/spotify-auth
   export SPOTIPY_CLIENT_ID=XxXxXxXxXxXxXxXxXxXxXxXxXxXxX
   export SPOTIPY_CLIENT_SECRET=XxXxXxXxXxXxXxXxXxXxXxXxXxXxX
   ```

4. The shell wrapper `spot.sh` sources the auth file before running the script.  We
   use it to run the python script.

   ```bash
   cd ~/bin
   ln -s $HOME/src/spot-playlists/spot.sh spot
   ```

5. The CLI will automatically use these environment variables for authentication.

### Usage
Show general help:

```bash
spot -h
```

User commands:

```bash
spot user info
```

Playlists commands:

```bash
spot playlists list
spot playlists create "My Playlist" -d "Optional description"
spot playlists tracks "My Playlist"
spot playlists add "My Playlist" "Dire Straits - Money For Nothing"
spot playlists remove "My Playlist" "Dire Straits - Money For Nothing"
```

Search tracks (supports stdin TSV with headers `artist` and `title` or `url`):

```bash
cat my-songs.tsv | spot search -
```

- All table outputs (playlists, tracks, search results) are printed in **tab-separated format** with lowercase headers.
- Tracks can be specified as Spotify URLs, URIs, or in the format `<artist> - <title>`.
- Using `-` as a song argument reads a table of songs from stdin for bulk operations.

### Notes
- Playlist references can be a name, URL, ID, or URI.
- Playlist names are cached in `~/.spotify/playlists` to allow name-based lookups.
- If a playlist name is not found in the cache, the CLI will query Spotify to refresh the cache.
- Automatic playlist updates using crontab are optional and can be configured by the user.
