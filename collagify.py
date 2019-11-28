# import spotipy
# import spotipy.util as util

import json
from flask import Flask, request, redirect, g, render_template
import requests
from urllib.parse import urlencode
app = Flask(__name__)


# Spotify URLs
spotify_auth_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
api_base_url = "https://api.spotify.com/v1"


# My Application Information
client_id = '4bdea43ff15c49be84c7a1ea44cc3ec7'
client_secret = 'my-secret-client-id'
redirect_uri = 'http://localhost:5000/callback'

params = urlencode({
                'client_id': client_id,
                'response_type': 'code',
                'redirect_uri': redirect_uri,
                'scope': 'user-follow-read user-top-read user-read-private',
                'show_dialog': 'true'
            })


@app.route('/')
def home_page():
    return render_template("index.html")


@app.route("/authorize")
def index():
    # Auth Step 1: Authorization
    return redirect(spotify_auth_url + '?' + params)


# Retrieve access and refresh tokens if authorization was successful.
@app.route('/callback')
def callback():
    auth_code = request.args['code']
    token_params = {
        'grant_type': 'authorization_code',
        'code': str(auth_code),
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }

    token_response = requests.post(token_url, data=token_params)
    print(f'Token status code: {token_response.status_code}')
    if token_response.status_code == 200:
        access_token = token_response.json()['access_token']
        expires_in = token_response.json()['expires_in']
        refresh_token = token_response.json()['refresh_token']
    else:
        return "Bad Request, Try Again"

    auth_header = {
        'Authorization': f'Bearer {access_token}'
    }

    # Requesting basic user data
    user_info_endpoint = api_base_url + '/me'
    user_api_response = requests.get(user_info_endpoint, headers=auth_header)
    user_name = user_api_response.json()['display_name']
    followers = user_api_response.json()['followers']['total']
    sub_type = user_api_response.json()['product']
    profile_url = user_api_response.json()['images'][0]['url']

    # Requesting user's listening history (Top Tracks/Artists)
    top_endpoint = api_base_url + '/me/top/tracks'
    top_params = {
        'limit': 9,
        'time_range': 'short_term'
    }

    top_response = requests.get(top_endpoint, headers=auth_header, params=top_params)
    artwork_list = []
    for top_track in top_response.json()['items']:
        # print(top_track['album']['images'])
        artwork_list.append(top_track['album']['images'][1]['url'])

    return render_template("user.html", username=user_name, followers=followers, sub_type=sub_type, profile_pic=profile_url, top_track=top_track, artwork_list=artwork_list)


if __name__ == "__main__":
    app.run(debug=True)
