import spotipy
import createPlaylist
import learnSongs
import requests
from urllib.parse import urlencode
import base64
import webbrowser

username = '20rem'

client_id = "2327937f76274679975195787e578210"
client_secret = "fa5d7fc7c5dd42d3b1467df13cf9e2cb"

auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": "http://localhost:7777/callback",
    "scope": "playlist-modify-public"
}

webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))

encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

print("Please supply the code in URL")
code = str(input())
print(code)

token_headers = {
    "Authorization": "Basic " + encoded_credentials,
    "Content-Type": "application/x-www-form-urlencoded"
}

token_data = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": "http://localhost:7777/callback"
}

r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

token = r.json()["access_token"]

if token:
    sp = spotipy.Spotify(auth=token)
    user = sp.current_user()

    while True:
        print("Welcome to the Song Recommender Based on Mood!")
        print("0-Create playlist based on your mood")
        print("1-Exit")
        print("")
        choice = input("Your choice: ")
        if choice == '0':
            mood = "happy" #here call a method getMood to get the emotion from video when ready
            print("Your mood is: ", mood)
            model = learnSongs.main()
            createPlaylist.main(sp, user, model, mood)
            print("Successfully created playlist!")
        if choice == '1':
            break
