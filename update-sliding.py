#!/usr/bin/python3

from helpers.config import read_config
from helpers.spotify import get_spotify 
from helpers.liked import get_previous_n_liked_songs

# given a playlist, returns the full tracklist as a list of track ids
def fetch_full_tracklist(spotify, playlist):
    tracklist = []
    results = spotify.playlist(playlist['id'], fields="tracks,next")
    spotify_tracks = results['tracks']
    while spotify_tracks:
        # not quite sure why the for loop is needed here
        for item in spotify_tracks['items']:
            spotify_track = item['track']
            tracklist.append(spotify_track['id'])
            
        spotify_tracks = spotify.next(spotify_tracks)
        
    return tracklist

# returns list of { "name": trackname, "uri": uri }
# containing each song in the spotify playlist provided
def get_tracklist(config, spotify, playlist_name):
    spotify_username = config["SPOTIFY_USERNAME"]
    playlists = spotify.user_playlists(spotify_username)
    tracklist = {}
    sliding_playlist_id = ""
    for playlist in playlists['items']:
        # defense against taking another user's playlist with the same name that 
        # you have liked not sure if this is even possible but why not
        if playlist['owner']['id'] != spotify_username:
            continue

        if playlist['name'] == playlist_name:
            tracklist = fetch_full_tracklist(spotify, playlist)
            sliding_playlist_id = playlist['id']
            break

    # by default these are sorted by most recent first, if I never rearrange the songs
    # in the playlist manually the invariant can be broken and the alg will break.
    # TODO account for that and go based off timestamps when added to the playlist (or
    # keep some state which tracks strict order of songs liked)

    return tracklist, sliding_playlist_id

# this script assumes you have liked at least n songs
def main():
    # get config
    config = read_config()

    # auth with spotify
    spotify = get_spotify(config)

    # get tracklist for sliding by least recent
    sliding_tracklist, sliding_playlist_id = get_tracklist(config, spotify, config["SPOTIFY_SLIDING_PLAYLIST"])

    # get liked songs sorted by most recent
    liked_songs = get_previous_n_liked_songs(config, spotify)

    # then make playlist changes
    i = 0
    while liked_songs[i] not in sliding_tracklist:
        # add liked song to spotify playlist
        spotify.playlist_add_items(sliding_playlist_id, [ liked_songs[i] ])

        # remove next item in sliding_tracklist from spotify playlist 
        spotify.playlist_remove_all_occurrences_of_items(sliding_playlist_id, [ sliding_tracklist[i] ])

        i += 1
    
    print(f'made {i} changes to {config["SPOTIFY_SLIDING_PLAYLIST"]}')

if __name__ == "__main__":
    main()