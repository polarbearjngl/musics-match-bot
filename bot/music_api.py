# coding=utf-8
import os
import requests
import json
from bot import Callbacks
from emoji import emojize

SUCCESS_CODE = 200
ERROR = emojize(u'Во время поиска что то пошло не так, либо поиск ничего не нашел :cry:', use_aliases=True)


class MusicMatch(object):
    """Class for sending requests to musixmatch"""

    TRACK_SEARCH = 'https://api.musixmatch.com/ws/1.1/track.search'

    def __init__(self):
        self._api_key = os.getenv("MUSICXMATCH_API_KEY")  # get variable from heroku environment vars
        self._actions = {Callbacks.TRACK_SEARCH: self._track_search,
                         Callbacks.ARTIST_SEARCH: self._artist_search,
                         Callbacks.LYRICS_SEARCH: self._lyrics_search}

    def _get(self, url, params=None, **kwargs):
        """Basic GET request"""
        params.update({'apikey': self._api_key})
        response = requests.get(url, params=params, **kwargs)

        return response if response.status_code == SUCCESS_CODE else None

    @property
    def get_actions(self):
        """Get encapsulated dict of methods"""
        return self._actions

    @staticmethod
    def _set_params(**kwargs):
        """Set params for request"""
        return {key: value for key, value in kwargs.items() if value}

    @staticmethod
    def _to_tracks(response_body):
        """Format response of request to text with tracks"""
        if response_body:
            content = json.loads(response_body.content)
            track_list = content['message']['body']['track_list']
            if track_list:
                return [Track(i).to_text() for i in track_list]

        return [ERROR]

    def _track_search(self, track, count=10, page=0, s_track_rating='desc'):
        """Search by track name"""
        params = self._set_params(**{
            'q_track': track, 'page_size': count, 'page': page, 's_track_rating': s_track_rating
        })
        return self._to_tracks(self._get(url=self.TRACK_SEARCH, params=self._set_params(**params)))

    def _artist_search(self, artist, count=10, page=0, s_artist_rating='desc'):
        """Search by artist name"""
        params = self._set_params(**{
            'q_artist': artist, 'page_size': count, 'page': page, 's_artist_rating': s_artist_rating
        })
        return self._to_tracks(self._get(url=self.TRACK_SEARCH, params=self._set_params(**params)))

    def _lyrics_search(self, lyrics, count=10, page=0):
        """Search by lyric name"""
        params = self._set_params(**{
            'q_lyrics': lyrics, 'page_size': count, 'page': page
        })
        return self._to_tracks(self._get(url=self.TRACK_SEARCH, params=self._set_params(**params)))


class Track(object):
    """Class for generating track object"""

    def __init__(self, track_info):
        self.album = track_info['track']['album_name']
        self.artist = track_info['track']['artist_name']
        self.track = track_info['track']['track_name']
        self.url_lyric = track_info['track']['track_share_url']

    def to_text(self):
        art_and_track_text = '<a href="{lyric}">{art} - {tra}</a>\n'.format(
            art=self.artist, tra=self.track, lyric=self.url_lyric)
        album_text = 'Альбом: {alb}\n\n'.format(alb=self.album)
        return "%s%s" % (art_and_track_text, album_text)
