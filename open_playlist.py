import json
import spotipy
import webbrowser

username = 'missframbuaz'
clientID = '322a5c047ccb4515b49404ed0d8f6065'
clientSecret = '7818fc966d344e6c82b36c7442f710ee'
redirectURI = 'http://google.com/' 
oauth_object = spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI)
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()
print(json.dumps(user,sort_keys=True, indent=4))
def openPlaylist(playlist_id):
    playlist = spotifyObject.playlist(playlist_id)
    webbrowser.open(playlist['external_urls']['spotify'])
    print('Playlist has opened in your browser.')

