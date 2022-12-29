import spotipy
import createPlaylist
import learnSongs


def run():
    client_id = "2327937f76274679975195787e578210"
    client_secret = "fa5d7fc7c5dd42d3b1467df13cf9e2cb"
    redirect_url = "http://localhost:7777/callback"

    oauth_object = spotipy.SpotifyOAuth(client_id, client_secret, redirect_url)
    token_dict = oauth_object.get_cached_token()
    token = token_dict['access_token']

    if token:
        sp = spotipy.Spotify(auth=token)
        user = sp.current_user()
        mood = "sad" #here use the result of face emotion detection part
        model = learnSongs.main()
        createPlaylist.main(sp, user, model, mood)
        print("Successfully created playlist!")