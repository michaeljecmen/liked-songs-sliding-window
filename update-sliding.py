#!/usr/bin/python3

from helpers.config import read_config
from helpers.cache import ConfigCacheHandler

# given a playlist, returns the full tracklist as a dict of uri->{name artists album}
def fetch_full_tracklist(spotify, playlist):
    tracklist = {}
    results = spotify.playlist(playlist['id'], fields="tracks,next")
    spotify_tracks = results['tracks']
    while spotify_tracks:
        # not quite sure why the for loop is needed here
        for item in spotify_tracks['items']:
            spotify_track = item['track']
            tracklist[spotify_track['uri']] = {
                "name": spotify_track['name'],
                "uri": spotify_track['uri'],
            }
            
        spotify_tracks = spotify.next(spotify_tracks)
        
    return tracklist

# returns list of { "name": trackname, "artists": [artists], "album": album }
# containing each song in the spotify playlist provided
def get_sliding_tracklist(config, spotify):
    spotify_username = config["SPOTIFY_USERNAME"]
    playlists = spotify.user_playlists(spotify_username)
    tracklist = {}
    for playlist in playlists['items']:
        # defense against taking another user's playlist with the same name that 
        # you have liked not sure if this is even possible but why not
        if playlist['owner']['id'] != spotify_username:
            continue

        if playlist['name'] == config["SPOTIFY_SLIDING_PLAYLIST"]:
            tracklist = fetch_full_tracklist(spotify, playlist)
            break

    # now sort by least recent TODO

    return tracklist

def main():
    # get config
    config = read_config()

    # auth with spotify
    oauth = SpotifyOAuth(client_id=config["SPOTIFY_CLIENT_ID"], client_secret=config["SPOTIFY_CLIENT_SECRET"], redirect_uri=config["SPOTIFY_REDIRECT_URI"], cache_handler=ConfigCacheHandler())
    spotify = spotipy.Spotify(oauth_manager=oauth)

    # get tracklist for sliding by least recent
    tracklist = get_sliding_tracklist(config, spotify)
    print(tracklist)

    # get liked songs sorted by most recent
    # for each liked_song in N most recent liked:
    #   if liked_song not in sliding
    #       add liked_song to sliding playlist
    #       remove least recent song from sliding playlist
    #       update internal dses

if __name__ == "__main__":
    main()