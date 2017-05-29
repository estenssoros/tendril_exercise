# coding: utf-8
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SebSpotipy(object):
    def __init__(self):
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    def get_top_track(self, uri):
        results = self.sp.artist_top_tracks(uri)
        tracks = results['tracks']
        if len(tracks) > 0:
            for track in tracks:
                if track.get('preview_url'):
                    return track['preview_url']
        return None

    def find_artist(self, name):
        '''
        given an artist name, return the first song and image url
        '''
        results = self.sp.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            image_url = artist['images'][0]['url']
            song = artist['id']
            uri = artist['uri']
            preview_url = self.get_top_track(uri)
            return {'image_url': image_url, 'preview_url': preview_url, 'uri': uri}
        return None

    def find_song(self, title):
        results = self.sp.search(q='track:' + title, type='track')
        items = results['tracks']['items']
        if len(items) > 0:
            track = items[0]
            uri = track['uri']
            preview_url = track['preview_url']
            image_url = track['album']['images'][0]['url']
            return {'uri': uri, 'preview_url': preview_url, 'image_url': image_url}

    def artist_track(self, artist, title):
        q = 'artist:{0} track:{1}'.format(artist.encode('utf-8'), title.encode('utf-8'))
        results = self.sp.search(q=q)
        tracks = results['tracks']['items']
        for track in tracks:
            uri = track['uri']
            image_url = track['album']['images'][0]['url']
            if track.get('preview_url'):
                return {'uri': uri, 'preview_url': track['preview_url'], 'image_url': image_url}
        return {'uri': uri, 'preview_url': None, 'image_url': image_url}


if __name__ == '__main__':
    artist = find_artist('Taylor Swift')
    song = find_song('Wildest Dreams')
