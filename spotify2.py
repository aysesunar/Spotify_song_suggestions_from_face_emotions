import spotipy
import createPlaylist
import learnSongs
from face_emotion_detection.emotion_detector_from_image import emotion_detector_from_image
import open_playlist
import json
def run():
    username = 'missframbuaz'
    clientID = '322a5c047ccb4515b49404ed0d8f6065'
    clientSecret = '7818fc966d344e6c82b36c7442f710ee'
    redirectURI = 'http://google.com/' 
    scope = 'user-library-read user-library-modify playlist-modify-public user-read-currently-playing user-read-playback-state user-modify-playback-state'
    oauth_object = spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI,scope=scope)
    token_dict = oauth_object.get_access_token()
    token = token_dict['access_token']
    spotifyObject = spotipy.Spotify(auth=token)
    user = spotifyObject.current_user()
    #print(json.dumps(user,sort_keys=True, indent=4))
    if token:
        sp = spotipy.Spotify(auth=token)
        user = sp.current_user()
        detector = emotion_detector_from_image()
        mood, frame = detector.detect_emotion() # "sad" #here use the result of face emotion detection part
        print(f'Mood is {mood}')
        model = learnSongs.main()
        playlist_id = createPlaylist.main(sp, user, model, mood, frame)
        print("Successfully created playlist!")
        
