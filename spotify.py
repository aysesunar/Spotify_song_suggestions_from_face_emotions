import spotipy
import createPlaylist
import learnSongs


def run():
    '''Irem:
    client_id = "2327937f76274679975195787e578210"
    client_secret = "fa5d7fc7c5dd42d3b1467df13cf9e2cb"
    redirect_url = "http://localhost:7777/callback"'''

    SPOTIFY_CLIENT_ID = "c58413b1659445f1be818dab581cd044"
    SPOTIFY_CLIENT_SECRET = "5fca9042f09d4f57a3a8e84f2e3a124a"
    SPOTIFY_REDIRECT_URI = "https://google.com"
    scope = 'user-library-read user-library-modify playlist-modify-public'

    oauth_object = spotipy.SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                        client_secret=SPOTIFY_CLIENT_SECRET,
                                        redirect_uri=SPOTIFY_REDIRECT_URI,
                                        scope=scope)

    token_dict = oauth_object.get_access_token()
    token = token_dict["access_token"]

    '''oauth_object = spotipy.SpotifyOAuth(client_id, client_secret, redirect_url)
    token_dict = oauth_object.get_cached_token()
    token = token_dict['access_token']'''

    if token:
        sp = spotipy.Spotify(auth=token)
        user = sp.current_user()
        mood = "sad" #here use the result of face emotion detection part
        model = learnSongs.main()
        createPlaylist.main(sp, user, model, mood)
        print("Successfully created playlist!")