import requests
import html
from core.utils import request
from bs4 import BeautifulSoup

class OVH(object):
    """
    OVH API object
    """
    def __init__(self, *args, **kwargs):
        self.base_url = "https://api.lyrics.ovh/v1/"


    def get_lyrics(self, artist, song):
        try:

            r = request(base_url=self.base_url, endpoint=f"{artist}/{song}")
            before = filter(None, r['lyrics'].replace('\r', '').split('\n'))
            after = list(before)
            return after
        except KeyError:
            return ["We searched for lyrics in the available APIs, but couldn't find the song.",
                    "Developer team has been warned about the song. Meanwhile please make sure that the song has lyrics."]