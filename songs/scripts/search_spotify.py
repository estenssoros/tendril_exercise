# coding: utf-8
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOauthError
from django.conf import settings

def replace_braces(s):
    braces = list('(){}[]')
    for b in braces:
        s = s.replace(b, '')
    return s


class SebSpotipy(object):
    def __init__(self):
        try:
            self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
            self.connected = True
        except SpotifyOauthError:
            self.connected = False

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
            image_url = artist['images'][0]['url'] if artist['images'] else settings.NO_IMAGE_URL
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
        artist = replace_braces(artist)
        title = replace_braces(title)
        q = 'artist:{0} track:{1}'.format(artist.encode('utf-8'), title.encode('utf-8'))
        results = self.sp.search(q=q)
        tracks = results['tracks']['items']
        uri, image_url = None, None
        for track in tracks:
            uri = track['uri']
            try:
                image_url = track['album']['images'][0]['url']
            except IndexError:
                image_url = None
            if track.get('preview_url'):
                return {'uri': uri, 'preview_url': track['preview_url'], 'image_url': image_url}
        return {'uri': uri, 'preview_url': None, 'image_url': image_url}


if __name__ == '__main__':
    seb = SebSpotipy()
    seb.find_artist('Snowpatrol')
