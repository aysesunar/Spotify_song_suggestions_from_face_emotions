import os
import json
import time
import spotipy

SPOTIFY_CLIENT_ID = "c58413b1659445f1be818dab581cd044"
SPOTIFY_CLIENT_SECRET = "5fca9042f09d4f57a3a8e84f2e3a124a"
SPOTIFY_REDIRECT_URI = "https://google.com"
scope = 'user-library-modify'

oauth_object = spotipy.SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                    client_secret=SPOTIFY_CLIENT_SECRET,
                                    redirect_uri=SPOTIFY_REDIRECT_URI,
                                    scope=scope)

token_dict = oauth_object.get_access_token()
token = token_dict["access_token"]

spotify_object = spotipy.Spotify(auth=token)

