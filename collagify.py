from flask import Flask, request, redirect, render_template, jsonify, session
from flask_session import Session
from urllib.parse import urlencode
import os
import requests
import json

app = Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


# Spotify URLs
spotify_auth_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
api_base_url = "https://api.spotify.com/v1"


# My Application Information
client_id = os.environ.get('client-id')
client_secret = os.environ.get('secret-id')
redirect_uri = 'https://spotify-collagify.herokuapp.com/callback'


auth_params = urlencode({
                'client_id': client_id,
                'response_type': 'code',
                'redirect_uri': redirect_uri,
                'scope': 'user-follow-read user-top-read user-read-private'
            })

# Login/Homepage
@app.route('/')
def home_page():
    return render_template("index.html")

# Authorize the user
@app.route("/authorize")
def index():
    return redirect(spotify_auth_url + '?' + auth_params)


# Retrieve access token from Spotify (needed to make API calls)
def get_access_token(code):
    token_params = {
        'grant_type': 'authorization_code',
        'code': str(code),
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }

    token_response = requests.post(token_url, data=token_params)
    if token_response.status_code < 300:
        access_token = token_response.json()['access_token']
        return access_token
    else:
        return None


# Get access token, request user data.
@app.route('/callback')
def callback():
    auth_code = request.args['code']
    token = get_access_token(auth_code)
    session['token'] = token

    if token:
        auth_header = {
            'Authorization': f'Bearer {token}'
        }

        # Requesting basic user data
        user_info_endpoint = api_base_url + '/me'
        user_api_response = requests.get(user_info_endpoint, headers=auth_header)
        user_name = user_api_response.json()['display_name']

        return render_template('user.html', username=user_name)
    else:
        # Do a re-login if user refreshes the page, or whenever there's a problem with the token.
        return redirect('/authorize')


# Get access token, request user listening history
@app.route('/collage', methods=['POST'])
def generate_collage():
    user_filters = request.form.to_dict()
    token = session['token']

    collage_type = user_filters['collage_type']
    time_frame = user_filters['time_frame']
    size = int(user_filters['size'])

    top_endpoint = api_base_url + f'/me/top/{collage_type}'
    top_params = {
        'limit': f'{size*size}',
        'time_range': time_frame
    }

    auth_header = {
        'Authorization': f'Bearer {token}'
    }

    top_response = requests.get(top_endpoint, headers=auth_header, params=top_params)
    artwork = {
        'items': []
    }

    if top_response.status_code >= 300:
        return json.dumps({'error': 'Unsuccessful request. Try refreshing the page.'})

    if collage_type == 'tracks':
        for item in top_response.json()['items']:
            artwork['items'].append({
                'name': item['name'],
                'url': item['album']['images'][1]['url']
                 })
    else:
        for item in top_response.json()['items']:
            artwork['items'].append({
                'name': item['name'],
                'url': item['images'][1]['url']
            })

    if len(artwork['items']) < size*size:
        return jsonify({'error': f'Not enough {collage_type} to create the collage! Please try a smaller size.'})

    return json.dumps(artwork)


if __name__ == "__main__":
    app.run(debug=True)