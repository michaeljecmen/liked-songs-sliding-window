
# return list of previous n liked songs, sorted with newest first
def get_previous_n_liked_songs(config, spotify):
    n = config["MAX_SLIDING_PLAYLIST_SIZE"]
    liked = []
    while len(liked) < n:
        # offset by number of songs we've already gathered
        resp = spotify.current_user_saved_tracks(offset=len(liked))
        liked.extend([ track['track']['id'] for track in resp['items'] ])
    
    # chop at n exactly
    return liked[:n]