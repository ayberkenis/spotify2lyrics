from flask import Flask, Blueprint, render_template, url_for, redirect, request, jsonify, Response, session, g
import logging
import core as s2lcore
from functools import wraps
import time
from pprint import pprint
import jinja2
import re

app = Flask(__name__)
app.secret_key = "r[AH=6z-$9)P9w.{"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['TESTING'] = False
app.config['SCHEDULER_API_ENABLED'] = False
app.config["REDIS_URL"] = "redis://localhost"
app.config['JSON_AS_ASCII'] = False
logging.basicConfig(filename='logs/spotify2lyrics.log', level=logging.NOTSET, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
auth = s2lcore.Spotify()
genius = s2lcore.Genius()
db = s2lcore.Database()
ovh = s2lcore.OVH()

@app.template_filter()
def regex_match(r):
    return re.match(r'\[(.*?)]', r)


def get_lyrics():
    """
    Check if lyrics exists in cache return from cache else perform a get request and parsing on api.
    :return:
    """
    player = auth.get_player_information()
    if hasattr(player, 'track'):
        check = db.check_if_exists(player.track.id)
        if check:
            return list(check)
        else:
            lyrics = genius.get_lyrics(query=f"{player.track.name}%20{player.track.artist.name}")
            if lyrics:
                db.insert_lyrics(player.track.artist.name, player.track.name, lyrics, player.track.id)
                return lyrics
            else:
                lyrics = ovh.get_lyrics(player.track.artist.name, player.track.name)
                db.insert_lyrics(player.track.artist.name, player.track.name, lyrics, player.track.id)
                return lyrics
    else:
        return ["You're not listening anything at the moment. To be able to see lyrics, you have to be listening a song in Spotify."]

def login_required(f):
    """
    Login required decorator to be able to make sure user has logged in and has their access_token saved in session.
    :param f:
    :return:
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session.keys() or auth.access_token is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def homepage():
    """
    Function name explains it very well.
    :return:
    """
    if auth.access_token and 'access_token' in session.keys():
        lyrics = get_lyrics()
        user = auth.get_user_profile()
        player = auth.get_player_information()
        return render_template("home.html", user=user, lyrics=lyrics, player=player)
    else:
        return render_template("layout-out.html", app_ = auth)


@app.route('/explore')
@login_required
def explore():
    """
    Function name explains it very well.
    :return:
    """
    user = auth.get_user_profile()
    return render_template("explore.html", user=user)

@app.route('/statistics')
@login_required
def statistics():
    """
    Function name explains it very well.
    :return:
    """
    user = auth.get_user_profile()
    top_artists = auth.get_top_artists()
    top_tracks = auth.get_top_tracks()
    recently_played = auth.get_recently_played()

    return render_template("statistics.html", tracks=top_tracks, artists=top_artists, recently_played=recently_played, user=user)


@app.route('/me')
@login_required
def user_profile():
    user = auth.get_user_profile()
    return render_template('profile.html', user=user)

@app.route('/playlists')
@login_required
def user_playlists():
    user = auth.get_user_profile()
    playlists = auth.get_playlists()
    player = auth.get_player_information()
    return render_template('playlists.html', user=user, playlists=playlists, player=player)

@app.route('/playlist/<id>')
@login_required
def playlist_wrap(id):
    user = auth.get_user_profile()
    playlist = auth.get_playlist(id)
    print(playlist)
    return render_template('single_playlist.html', user=user, playlist=playlist)

@app.route('/login')
def login():
    """
    Login URL
    :return:
    """
    url = auth.build_url()
    return redirect(url)

@app.route('/api/v1/serve-live-data/')
def serve_live_data():
    """
    Static data as HTML body, call it in homepage with an ajax request every interval
    :return:
    """
    if auth.access_token and 'access_token' in session.keys():
        lyrics = get_lyrics()
        player = auth.get_player_information()
        return render_template("live-api.html", lyrics=lyrics, player=player)

@app.route('/api/v1/serve-data/')
def serve_data():
    """
    Static data as HTML body, call it in homepage with an ajax request every interval
    :return:
    """
    if auth.access_token and 'access_token' in session.keys():
        lyrics = get_lyrics()
        player = auth.get_player_information()

        return jsonify(player.data, lyrics)



@app.route('/callback')
def callback():
    """
    Callback route for spotify authorization
    Get 'code' from the URL, exchange it with access_token and save it to session for further usage
    """
    code = request.args.get('code')
    access_token = auth.exchange_code_to_access_token(code)
    session['access_token'] = access_token
    return redirect(url_for('homepage'))


@app.route("/logs")
@login_required
def logs():
    """[FOR DEBUG PURPOSES]"""
    return render_template("logs.html")

@app.route('/log-stream')
def stream():
    """[FOR DEBUG PURPOSES]"""
    def generate():
        with open('logs/spotify2lyrics.log') as f:
            while True:
                yield f.read()
                time.sleep(1)

    return app.response_class(generate(), mimetype='text/plain')


@app.route('/logout')
def logout():
    """
    Logs out the current user by clearing the session access_token
    :return:
    """
    session.clear()
    auth.access_token = None
    return redirect(url_for('homepage'))

@app.errorhandler(404)
def not_found(e):
    user = auth.get_user_profile()
    return render_template('404.html', user=user, e=e), 404


if __name__ == '__main__':

    app.run(debug=True)
