import spotipy


def get_top_track(uri):
    spotify = spotipy.Spotify()
    results = spotify.artist_top_tracks(uri)
    tracks = results['tracks']
    if len(tracks) > 0:
        for track in tracks:
            if track.get('preview_url'):
                return track['preview_url']
    return None


def find_artist(name):
    '''
    given an artist name, return the first song and image url
    '''
    spotify = spotipy.Spotify()
    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        image_url = artist['images'][0]['url']
        song = artist['id']
        uri = artist['uri']
        preview_url = get_top_track(uri)
        return {'image_url': image_url, 'preview_url': preview_url, 'uri': uri}
    return None


def find_song(title):
    spotify = spotipy.Spotify()
    results = spotify.search(q='track:' + title, type='track')
    items = results['tracks']['items']
    if len(items) > 0:
        track = items[0]
        uri = track['uri']
        preview_url = track['preview_url']
        image_url = track['album']['images'][0]['url']
        return {'uri': uri, 'preview_url': preview_url, 'image_url': image_url}


if __name__ == '__main__':
    artist = find_artist('Taylor Swift')
    song = find_song('Wildest Dreams')
