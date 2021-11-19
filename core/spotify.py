import datetime
import requests
import json
from core.utils import request
import uuid



class Spotify(object):
    """
    Spotify Object
    """
    def __init__(self):
        self.access_token = None
        self.access_token_expires = datetime.datetime.now()
        self.access_token_did_expire = True
        self.client_id = "YOUR CLIENT ID"
        self.client_secret = "YOUR CLIENT SECRET"
        self.redirect_uri = "http://127.0.0.1:5000/callback"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.scopes = "user-read-currently-playing user-read-playback-state " \
                      "user-follow-modify user-follow-read " \
                      "user-read-playback-position " \
                      "user-read-recently-played user-top-read user-read-playback-position " \
                      "ugc-image-upload playlist-modify-private playlist-read-private playlist-modify-public user-library-read user-follow-read"
        self.access = False
        self.base_url = "https://api.spotify.com/v1/"
        self.version = "v0.4.1"


    def build_url(self):
        scopes = self.scopes.replace(' ', '%20')
        state = str(uuid.uuid4())[8]
        url = f"https://accounts.spotify.com/authorize?client_id={self.client_id}&response_type=code&redirect_uri={self.redirect_uri}&scope={scopes}&state={state}"
        return url

    def exchange_code_to_access_token(self, code):
        """
        Requires code param to be able to exchange code to access_token
        :param code:
        :return:
        """
        params = {"code": code, "redirect_uri": self.redirect_uri, "grant_type": "authorization_code",
                  "client_id": self.client_id, "client_secret": self.client_secret, "scope": self.scopes}
        r = requests.post(self.token_url, params)
        js = json.loads(r.content)
        if "access_token" in js.keys():
            self.access_token = js['access_token']
            self.access = True
        else:
            self.access_token = None
            self.access = False
        return self.access_token

    def get_user_profile(self):
        """
        Performs a GET request to /me endpoint
        :return:
        """
        r = request(self.base_url, self.access_token, "me", None)
        return User(r)

    def get_album(self, aid):
        """
        Performs a GET request to /albums endpoint
        :param aid:
        :return:
        """
        r = request(self.base_url,self.access_token, "albums", f"{aid}")
        return Album(r)

    def get_artist(self, aid):
        """
        Performs a GET request to /artists endpoint
        :param aid:
        :return:
        """
        r = request(self.base_url,self.access_token, "artists", f"id={aid}")
        return Artist(r)

    def get_player_information(self):
        """
        Performs a GET request to /me/player endpoint
        :return:
        """
        r = request(self.base_url,self.access_token, "me/player")
        return Player(r)


    def get_users_available_devices(self):
        """
        Gets user's available devices
        :return:
        """
        return request(self.base_url,self.access_token, "me/player", f"devices")


    def get_playlists(self):
        """
        Get user's playlists
        :return:
        """
        r = request(self.base_url, self.access_token, "me/playlists" f"?limit=50")
        return Playlist(r)

    def get_playlist(self, pid):
        """
        Gets a single playlist
        :param pid:
        :return:
        """
        return request(self.base_url, self.access_token, f"playlists/{pid}")

    def get_top_artists(self):
        """
        Gets user's top artists long term with 50 limit
        :return:
        """
        r = request(self.base_url, self.access_token, "me/top/artists?limit=50&time_range=long_term")
        return [Artist(item) for item in r['items']]

    def get_top_tracks(self):
        """
        Gets user's top tracks long term with 50 limit
        :return:
        """
        r = request(self.base_url, self.access_token, "me/top/tracks?limit=50&time_range=long_term")
        return [Track(item) for item in r['items']]

    def get_recently_played(self):
        """
        Gets user's listening history
        :return:
        """
        r = request(self.base_url, self.access_token, "me/player/recently-played?limit=50&time_range=long_term")
        return [Track(item['track']) for item in r['items']]

class User:
    """
    User Model
    """
    def __init__(self, data):
        self.data = data
        try:
            self.display_name = self.data['display_name']
            self.country = self.data['country']
            self.email = self.data['email']
            self.exp_filter_enabled = self.data['explicit_content']['filter_enabled']
            self.exp_filter_locked = self.data['explicit_content']['filter_locked']
            self.external_url_spotify = self.data['external_urls']['spotify']
            self.followers = self.data['followers']['total']
            self.id = self.data['id']
            self.avatar_url = self.data['images'][0]['url']
            self.uri = self.data['uri']
            self.product = self.data['product']
        except KeyError or TypeError:
            pass

class Player:
    """
    Player Model
    """
    def __init__(self, data):

        self.data = data
        try:
            self.device = self.data['device']['name']
            self.device_type = self.data['device']['type']
            self.is_active = self.data['device']['is_active']
            self.volume = self.data['device']['volume_percent']
            self.id = self.data['device']['id']
            self.is_private = self.data['device']['is_private_session']
            self.is_restricted = self.data['device']['is_restricted']
            self.timestamp = self.data['timestamp']
            self.repeat_state = self.data['repeat_state']
            self.is_shuffle = self.data['shuffle_state']
            # self.ctx = self.data['context']['type']
            # self.ctx_external_url = self.data['context']['external_urls']['spotify']
            self.progress_ms = self.data['progress_ms']
            self.track = Track(self.data['item'])
            self.duration_ms = self.data['item']['duration_ms']
            self.currently_playing_type = self.data['currently_playing_type']
        except KeyError or TypeError:
            pass


class Album:
    """
    Album Model
    """
    def __init__(self, data):
        self.data = data
        try:
            self.album_type = self.data['album_type']
            self.total_tracks = self.data['total_tracks']
            self.href = self.data['href']
            self.id = self.data['id']
            self.image = self.data['images'][0]['url']
            self.name = self.data['name']
            self.release_date = self.data['release_date']
            self.artist = Artist(self.data['artists'])
        except KeyError or TypeError:
            pass

class Artist:
    """
    Artist Model
    """
    def __init__(self, data):
        if isinstance(data, list):
            self.data = data[0]
            try:
                self.external_url = self.data['external_urls']['spotify']
                self.href = self.data['href']
                self.id = self.data['id']
                self.name = self.data['name']
                self.uri = self.data['uri']
                self.avatar = self.data['images'][0]['url']
            except KeyError or TypeError:
                pass
        else:
            self.data = data
            self.external_url = self.data['external_urls']['spotify']
            self.href = self.data['href']
            self.id = self.data['id']
            self.name = self.data['name']
            self.uri = self.data['uri']
            self.avatar = self.data['images'][0]['url']

class Track:
    """
    Track Model
    """
    def __init__(self, data):
        self.data = data
        try:
            self.album = Album(self.data['album'])
            self.artist = Artist(self.data['artists'])
            self.duration_ms = self.data['duration_ms']
            self.is_explicit = self.data['explicit']
            self.href = self.data['href']
            self.id = self.data['id']
            self.is_local = self.data['is_local']
            self.name = self.data['name']
            self.popularity = self.data['popularity']
            self.track_number = self.data['track_number']
            self.uri = self.data['uri']
            self.isrc = self.data['external_ids']['isrc']
        except KeyError or TypeError:
            pass


class Playlist:
    """
    Playlist Model
    """
    def __init__(self, data):
        self.data = data['items']
        try:
            if isinstance(self.data, list):
                for p in self.data:
                    self.is_collaborative = p['collaborative']
                    self.description = p['description']
                    self.followers = p['followers']['total']
                    self.href = p['href']
                    self.id = p['id']
                    self.image = p['images'][0]['url']
                    self.owner = User(p['owner'])
                    self.is_public = p['public']
                    self.tracks = Track(p['tracks'])
                    self.uri = p['uri']
                    self.name = p['name']
        except KeyError or TypeError:
            pass

class Category:
    """
    Category Model
    """
    def __init__(self, data):
        self.data = data


class Genre:
    """
    Genre Model
    """
    def __init__(self, data):
        self.data = data
