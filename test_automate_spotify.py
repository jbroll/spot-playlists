import unittest
from unittest.mock import patch
from automate_spotify import *


class TestAutomateSpotify(unittest.TestCase):
    @patch('automate_spotify.sp.current_user')
    def test_view_user_info(self, mock_current_user):
        # Arrange
        mock_current_user_data = {
            "display_name": "John Doe",
            "followers": {"total": 100}
        }
        mock_current_user.return_value = mock_current_user_data

        with patch("builtins.print") as mock_print:
            # Act
            user = view_user_info()
            # Assert
            mock_print.assert_any_call("--User Info--")
            mock_print.assert_any_call("Name:", "John Doe")
            mock_print.assert_any_call("Total followers:", 100)

        self.assertEqual(user["display_name"], "John Doe")
        self.assertEqual(user["followers"]["total"], 100)

    @patch('automate_spotify.sp.current_user_playlists')
    def test_view_user_playlist(self, mock_current_user_playlist):
        # Arrange
        mock_current_user_playlist_data = {
            "items": [{
                "name": "Mock Playlist Name",
                "id": "Mock ID",
                "description": "Mock description",
                "tracks": {
                    "total": 100
                }
            }]
        }
        mock_current_user_playlist.return_value = mock_current_user_playlist_data
        # Act
        with patch("builtins.print") as mock_print:
            user_playlists = view_user_playlists()
        # Assert
            mock_print.assert_any_call("--User Current Playlists--")
            mock_print.assert_any_call("Playlist's name:", "Mock Playlist Name")
            mock_print.assert_any_call("Playlist's ID:", "Mock ID")
            mock_print.assert_any_call("Playlist's description:", "Mock description")
            mock_print.assert_any_call("Total tracks:", 100)
        self.assertEqual(user_playlists, mock_current_user_playlist_data)

    @patch('automate_spotify.sp.current_user_saved_tracks')
    def test_view_user_saved_tracks(self, mock_current_user_saved_tracks):
        # Arrange
        mock_current_user_saved_tracks_data = {
            "items": [
                {
                    "track": {
                        "name": "Mock name",
                        "album": {"name": "Mock album name"},
                        "artists": [{"name": "Mock artist name"}]
                    }
                }
            ]
        }
        mock_current_user_saved_tracks.return_value = mock_current_user_saved_tracks_data
        # Act
        with patch("builtins.print") as mock_print:
            user_saved_tracks = view_user_saved_tracks(amount=1)
        # Arrange
            mock_print.assert_any_call("--User Current Saved Tracks--")
            mock_print.assert_any_call("Track's name:", "Mock name")
            mock_print.assert_any_call("Track's album:", "Mock album name")
            mock_print.assert_any_call("Track's artist:", "Mock artist name")
        self.assertEqual(user_saved_tracks, mock_current_user_saved_tracks_data)

    @patch('automate_spotify.sp.playlist')
    def test_view_weekly_discovery_tracks(self, mock_playlist):
        # Arrange
        mock_playlist_data = {
            "tracks": {
                "items": [
                    {"track": {
                        "name": "Mock track name",
                        "artists": [{"name": "Mock artist name"}],
                        "id": "Mock ID"
                    }}
                ]
            }
        }
        mock_playlist.return_value = mock_playlist_data
        # Act
        with patch("builtins.print") as mock_print:
            weekly_playlist = view_weekly_discovery_tracks()
        # Assert
        mock_print.assert_any_call("---Discover Weekly Tracks---")
        mock_print.assert_any_call("Track's name:", "Mock track name")
        mock_print.assert_any_call("Artist:", "Mock artist name")
        mock_print.assert_any_call("Track's ID:", "Mock ID")
        self.assertEqual(weekly_playlist, mock_playlist_data)

    @patch('automate_spotify.sp.playlist')
    def test_view_day_list_tracks(self, mock_playlist):
        # Arrange
        mock_playlist_data = {
            "tracks": {
                "items": [
                    {"track": {
                        "name": "Mock track name",
                        "artists": [{"name": "Mock artist name"}],
                        "album": {"name": "Mock album name"}
                    }}
                ]
            }
        }
        mock_playlist.return_value = mock_playlist_data
        # Act
        with patch("builtins.print") as mock_print:
            user_day_list_playlist = view_day_list_tracks()
        # Assert
        mock_print.assert_any_call("---Current Day List Tracks---")
        mock_print.assert_any_call("Name:", "Mock track name")
        mock_print.assert_any_call("Artist:", "Mock artist name")
        mock_print.assert_any_call("Album:", "Mock album name")
        self.assertEqual(user_day_list_playlist, mock_playlist_data)

    @patch('automate_spotify.sp.current_user_playlists')
    @patch('automate_spotify.sp.current_user')
    @patch('automate_spotify.sp.user_playlist_create')
    def test_create_playlist_successful(self, mock_user_playlist_create, mock_current_user, mock_current_user_playlists):
        mock_current_user_data = {"id": "mock id"}
        mock_current_user.return_value = mock_current_user_data
        mock_user_playlist_create_data = {'collaborative': False,
                                          'description': '',
                                          'external_urls': {'spotify': 'mock spotify'},
                                          'followers': {'href': None, 'total': 0},
                                          'href': 'mock href',
                                          'id': 'mock id',
                                          'images': [],
                                          'name': 'mock name',
                                          'owner': {'display_name': 'mock owner name',
                                                    'external_urls': {'spotify': 'mock spotify'},
                                                    'href': 'mock href',
                                                    'id': 'mock id',
                                                    'type': 'user',
                                                    'uri': 'mock uri'},
                                          'primary_color': None,
                                          'public': True,
                                          'snapshot_id': 'mock snapshot id',
                                          'tracks': {'href': 'mock href',
                                                     'items': [],
                                                     'limit': 100,
                                                     'next': None,
                                                     'offset': 0,
                                                     'previous': None,
                                                     'total': 0},
                                          'type': 'playlist',
                                          'uri': 'mock uri'}
        mock_user_playlist_create.return_value = mock_user_playlist_create_data
        with patch("builtins.print") as mock_print:
            new_playlist = create_playlist(name="mock name", description="")
        mock_print.assert_any_call("Playlist mock name has been created")
        self.assertEqual(new_playlist, mock_user_playlist_create_data)

    @patch('automate_spotify.sp.current_user_playlists')
    @patch('automate_spotify.sp.current_user')
    def test_create_playlist_fail(self, mock_current_user, mock_current_user_playlists):
        mock_current_user_data = {"id": "mock user id"}
        mock_current_user.return_value = mock_current_user_data
        mock_current_user_playlists_data = {
            "items": [
                {"name": "mock name"}
            ]
        }
        mock_current_user_playlists.return_value = mock_current_user_playlists_data
        with patch("builtins.print") as mock_print:
            new_playlist = create_playlist(name="mock name", description="")
        mock_print.assert_any_call("Playlist name already exists. Please choose another one")
        self.assertEqual(new_playlist, None)

    @patch('automate_spotify.sp.playlist_add_items')
    def test_add_songs_to_playlist(self, mock_playlist_add_items):
        mock_playlist_add_items_data = {"snapshot_id": "mock snapshot_id"}
        mock_playlist_add_items.return_value = mock_playlist_add_items_data

        with patch("builtins.print") as mock_print:
            playlist = add_songs_to_playlist(playlist_id="mock playlist_id",items=["songs"])
        mock_print.assert_any_call("Songs have been added to the playlist.")
        mock_playlist_add_items.assert_called_with(playlist_id="mock playlist_id",items=["songs"])
        self.assertEqual(playlist, mock_playlist_add_items_data)

    @patch('automate_spotify.sp.playlist_add_items')
    @patch('automate_spotify.sp.playlist_items')
    def test_add_songs_from_daylist_playlist(self, mock_playlist_items, mock_playlist_add_items):
        # Mock data for playlist_items response
        mock_weekly_tracks_data = {
            "items": [
                {"track": {"id": "track1_id"}},
                {"track": {"id": "track2_id"}}
            ]
        }
        mock_playlist_items.return_value = mock_weekly_tracks_data

        # Mock data for playlist_add_items response
        mock_add_items_response = "Mocked add items response"
        mock_playlist_add_items.return_value = mock_add_items_response

        # The playlist ID to add songs to
        test_playlist_id = "test_playlist_id"

        # Mocking the print function
        with patch("builtins.print") as mock_print:
            response = add_songs_from_daylist_playlist(playlist_id=test_playlist_id)

        # Assert playlist_items was called correctly
        mock_playlist_items.assert_called_once_with(
            playlist_id="https://open.spotify.com/playlist/37i9dQZF1EP6YuccBxUcC1?si=f5d4859eafbd461c")

        # Assert playlist_add_items was called with extracted track IDs
        mock_playlist_add_items.assert_called_once_with(playlist_id=test_playlist_id, items=["track1_id", "track2_id"])

        # Assert correct print statement
        mock_print.assert_called_once_with("All songs from current Day List Playlist have been added.")

        # Assert the correct response is returned
        self.assertEqual(response, mock_add_items_response)

    @patch('automate_spotify.sp.playlist_add_items')
    @patch('automate_spotify.sp.playlist_items')
    def test_add_songs_from_weekly_playlist(self, mock_playlist_items, mock_playlist_add_items):
        # Mock data for playlist_items response
        mock_weekly_tracks_data = {
            "items": [
                {"track": {"id": "track1_id"}},
                {"track": {"id": "track2_id"}}
            ]
        }
        mock_playlist_items.return_value = mock_weekly_tracks_data

        # Mock data for playlist_add_items response
        mock_add_items_response = "Mocked add items response"
        mock_playlist_add_items.return_value = mock_add_items_response

        # The playlist ID to add songs to
        test_playlist_id = "test_playlist_id"

        # Mocking the print function
        with patch("builtins.print") as mock_print:
            response = add_songs_from_weekly_playlist(playlist_id=test_playlist_id)

        # Assert playlist_items was called correctly
        mock_playlist_items.assert_called_once_with(
            playlist_id="https://open.spotify.com/playlist/37i9dQZEVXcSl5JcFboUlo")

        # Assert playlist_add_items was called with extracted track IDs
        mock_playlist_add_items.assert_called_once_with(playlist_id=test_playlist_id, items=["track1_id", "track2_id"])

        # Assert correct print statement
        mock_print.assert_called_once_with("All songs from this week Discover Weekly Playlist have been added.")

        # Assert the correct response is returned
        self.assertEqual(response, mock_add_items_response)

    @patch('automate_spotify.sp.playlist_items')
    def test_view_playlist_tracks(self, mock_playlist_items):
        mock_playlist_items_data = {
            "items": [
                {"track": {
                    "name": "track 1",
                    "album": {"name": "album 1"},
                    "artists": [{"name": "artist 1"}]
                }}
            ]
        }
        mock_playlist_items.return_value = mock_playlist_items_data
        with patch("builtins.print") as mock_print:
            playlist_tracks = view_playlist_tracks(playlist_id ="mock playlist_id")
        mock_print.assert_any_call("Name:", "track 1")
        mock_print.assert_any_call("Album:", "album 1")
        mock_print.assert_any_call("Artist:", "artist 1")
        mock_playlist_items.assert_called_with(playlist_id="mock playlist_id")
        self.assertEqual(playlist_tracks, mock_playlist_items_data)


if __name__ == "__main__":
    unittest.main()