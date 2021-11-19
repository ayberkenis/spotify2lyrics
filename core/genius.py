import requests
import html
from core.utils import request
from bs4 import BeautifulSoup


class Genius(object):
    """
    Genius API object
    """
    def __init__(self, *args, **kwargs):
        self.access_token = "YOUR ACCESS TOKEN"
        self.client_id = "YOUR CLIENT ID"
        self.client_secret = "YOUR CLIENT SECRET"
        self.base_url = "https://api.genius.com/"



    def search(self, query):
        """
        Search on Genius API to get results
        :param query:
        :return:
        """
        return request(self.base_url, self.access_token, f"search?q=", query)

    def get_lyrics_url(self, query:str):
        """
        Choose first element of the search results
        :param query:
        :return:
        """
        query = query.replace(" ", "%20")
        res = self.search(query)

        if res['response']['hits']:
            result = res['response']['hits'][0]
            if result['index'] == "song":
                if result['result']:
                    r = request(self.base_url, self.access_token, f"songs/{result['result']['id']}")
                    return r['response']['song']['url']
        else:
            return None

    def get_lyrics(self, query):
        """
        Parse lyrics from the HTML with BeautifulSoup
        :param query:
        :return:
        """
        try:
            if query:
                url = self.get_lyrics_url(query)

                soup = BeautifulSoup(requests.get(url).content, 'lxml')

                for tag in soup.select('div[class^="Lyrics__Container"], .song_body-lyrics p'):
                    t = tag.get_text(strip=True, separator='<br>')
                    if t:
                        lyrics = t.split('<br>')
                        return lyrics
        except Exception:
            pass



