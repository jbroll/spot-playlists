#!/bin/sh
#

# Store you credentialy here
#
. $HOME/.spotify/spotify-auth

$HOME/src/spot-playlists/bin/python \
        $HOME/src/spot-playlists/spot.py "$@"
