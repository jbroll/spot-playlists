import argparse
from automate_spotify import *


def main():
    parser = argparse.ArgumentParser(description="A Python CLI tool for managing Spotify playlists and tracks.")
    parser.add_argument("-u", "--user", action="store_true", help="Display the user's Spotify profile information.")
    parser.add_argument("-p", "--playlists", action="store_true", help="List all playlists in the user's Spotify account.")
    parser.add_argument("-t", "--tracks", type=int, help="Display a specified number of saved tracks from the user's account.")
    parser.add_argument("-w", "--weekly", action="store_true", help="Show the user's Discover Weekly playlist curated by Spotify.")
    parser.add_argument("-d", "--daylist", action="store_true", help="Show the user's current Day List Playlist curated by Spotify.")
    parser.add_argument("-c", "--create", type=str, help="Create a new playlist. Playlist's name is required and description is optional.")
    parser.add_argument("-a", "--add", type=str, help="Add songs to an existing playlist. Enter playlist's URL.")
    parser.add_argument("-ad", "--adddaylist", type=str, help="Add tracks from Day List to a specified playlist. Enter playlist's URL.")
    parser.add_argument("-aw", "--addweekly", type=str, help="Add tracks from Discover Weekly to a specified playlist. Enter playlist's URL.")

    parser.add_argument("-de", "--description", type=str, help="Set a description for a new playlist being created.")
    parser.add_argument("-so", "--songs", type=str, nargs="+", help="Add a list of songs URLs to a specified playlist.")

    args = parser.parse_args()

    if args.user:
        print("*** You are viewing user info ***")
        view_user_info()
    elif args.playlists:
        print("*** You are viewing user playlists ***")
        view_user_playlists()
    elif args.tracks:
        print("*** You are viewing user saved tracks ***")
        view_user_saved_tracks(args.tracks)
    elif args.weekly:
        print("*** You are viewing this week Discover Weekly playlist's tracks ***")
        view_weekly_discovery_tracks()
    elif args.daylist:
        print("*** You are viewing user's current Day List playlist's track ***")
        view_day_list_tracks()
    elif args.create:
        print("*** New playlist is being created ***")
        create_playlist(args.create, args.description)
    elif args.add and args.songs:
        print("*** Songs are being added to your playlist ***")
        add_songs_to_playlist(args.add, args.songs)
    elif args.adddaylist:
        print("*** Songs from Day List playlist have been added to your playlist ***")
        add_songs_from_daylist_playlist(args.adddaylist)
    elif args.addweekly:
        print("*** Songs from Discover Weekly playlist have been added to your playlist ***")
        add_songs_from_weekly_playlist(args.addweekly)
    else:
        print("Invalid command.")


if __name__ == "__main__":
    main()