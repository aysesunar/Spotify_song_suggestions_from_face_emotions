import json
import spotipy
import webbrowser
import createPlaylist

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
def playlist_playback(sp, device, context_uri, offset, ms):
    sp.start_playback(device_id=device, context_uri=context_uri, offset=offset, position_ms=ms)
def openPlaylist(playlist_id):
    playlist = spotifyObject.playlist(playlist_id)
    webbrowser.open(playlist['external_urls']['spotify'])
    print('Playlist has opened in your browser.')

    context_uri = "spotify:playlist:" + playlist_id
    offset = {"position": 0}
    res = spotifyObject.devices()
    first_device = res['devices'][0].get('id') 
    try:
        playlist_playback(spotifyObject, first_device, context_uri, offset, ms=1)
    except Exception as e:
        print(e)

