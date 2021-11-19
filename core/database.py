import json

class Database:
    def __init__(self):
        with open('./data/song_cache.json', 'r') as f:
            self.data = json.load(f)



    def check_if_exists(self, song_id):
        if song_id in self.data.keys():
            return self.data[song_id]['lyrics']

    def insert_lyrics(self, artist, song, lyrics, song_id):
        if song_id not in self.data.keys():
            data = {'artist': artist, 'song': song, 'lyrics': lyrics}
            self.data[song_id] = data
            with open('./data/song_cache.json', 'w', encoding="utf8") as f:
                json.dump(self.data, f, indent=2)

