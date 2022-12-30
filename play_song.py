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
        # Get the Song Name.
        searchQuery = input("Enter Playlist Name: ")
        # Search for the Song.
        searchResults = spotifyObject.search(searchQuery,2,0,"playlist")
        print(searchResults)
        #print(searchResults)
        # Get required data from JSON response.
        tracks_dict = searchResults['playlists']
        tracks_items = tracks_dict['items']
        song = tracks_items[0]['external_urls']['spotify']
        # Open the Song in Web Browser
        webbrowser.open(song)
        print('Song has opened in your browser.')
    elif choice == 0:
        break
    else:
        print("Enter valid choice.")

'''
import pyautogui 
import os
import time
os.system("spotify")
time.sleep(5)
pyautogui.hotkey('ctrl','l')
pyautogui.write('Endure the silence',interval=0.1)

for key in ['enter', 'pagedown', 'tab','enter','enter']:
    time.sleep(2)
'''
