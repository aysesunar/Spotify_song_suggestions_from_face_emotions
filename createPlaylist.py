import numpy as np
import time
from PIL import Image
import base64
import open_playlist
def getUserTracks(sp):
    results = []
    trackURIs = []
    tracks = []

    numTracks = 100
    maxObjects = 50
    for i in range(numTracks // maxObjects):
        savedTracks = sp.current_user_saved_tracks(limit=maxObjects, offset=i * maxObjects)
        if savedTracks != None:
            results.append(savedTracks)

    for item in results:
        for info in item['items']:
            trackURIs.append(info['track']['uri'])
            tracks.append(info['track']['name'] + " by " + info['track']['artists'][0]['name'])
    return trackURIs, tracks


def getAudioFeatures(sp, trackURIs):
    features = []
    featuresTotal = []
    max = 100
    for i in range(0, len(trackURIs), max):
        audioFeatures = sp.audio_features(trackURIs[i:i + max])
        time.sleep(1)
        for j in range(len(audioFeatures)):
            if audioFeatures[j] != None:
                features.append(audioFeatures[j]['danceability'])
                features.append(audioFeatures[j]['energy'])
                features.append(audioFeatures[j]['valence'])
                featuresTotal.append(features)
            features = []
    return featuresTotal


def createPlaylist(sp, user, trackURIs, features, mood, model, frame):
    featuresArray = np.asarray(features, dtype=np.float32)
    predictions = model.predict(featuresArray)
    playlistSongs = []

    for i in range(len(predictions)):
        if predictions[i] == mood:
            playlistSongs.append(trackURIs[i])
        if len(playlistSongs) >= 30:
            break
    userID = user['id']
    playlist = sp.user_playlist_create(userID, name=mood, public=True)
    playlistID = playlist['id']
    if playlist['images'] == []:
        try:
            sp.playlist_upload_cover_image(playlistID, frame)
        except:
            print("Couldn't add cover image to playlist")

    sp.user_playlist_add_tracks(userID, playlistID, playlistSongs)
    print(playlistID)
    return playlistID


def main(sp, user, model, mood, frame):
    trackURIs, tracks = getUserTracks(sp)
    features = getAudioFeatures(sp, trackURIs)
    playlist_id = createPlaylist(sp, user, trackURIs, features, mood, model, frame)
    open_playlist.openPlaylist(playlist_id)
