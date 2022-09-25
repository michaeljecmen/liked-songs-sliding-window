#!/usr/bin/python3

from helpers.spotify import get_spotify
from helpers.config import read_config
from helpers.liked import get_previous_n_liked_songs
from helpers.playlist import find_playlist

def populate_playlist():
    config = read_config()
    spotify = get_spotify(config)
    liked = get_previous_n_liked_songs(config, spotify)

    playlist = find_playlist(config, spotify, config["SPOTIFY_SLIDING_PLAYLIST"])

    # we want to add the items so future queries will appear oldest first
    # if we add the items all at the same time, they'll be newest first
    liked.reverse()

    spotify.playlist_add_items(playlist['id'], liked)

if __name__ == "__main__":
    populate_playlist()