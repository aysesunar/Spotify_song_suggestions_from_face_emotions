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
while True:
    print("Welcome, "+ user['display_name'])
    print("0 - Exit")
    print("1 - Search for a Playlist")
    choice = int(input("Your Choice: "))
    if choice == 1:
        searchQuery = input("Enter Playlist Id: ")
        #example id=0mh2I0USWjpJkwe95XdqCU
        playlist = spotifyObject.playlist(searchQuery)
        webbrowser.open(playlist['external_urls']['spotify'])
        print('Playlist has opened in your browser.')
    elif choice == 0:
        break
    else:
        print("Enter valid choice.")
