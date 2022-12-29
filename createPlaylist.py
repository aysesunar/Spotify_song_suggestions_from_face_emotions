import numpy as np
import time


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
            if audioFeatures != None:
                features.append(audioFeatures[j]['danceability'])
                features.append(audioFeatures[j]['energy'])
                features.append(audioFeatures[j]['valence'])
                featuresTotal.append(features)
            features = []
    return featuresTotal


def createPlaylist(sp, user, trackURIs, features, mood, model):
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
    sp.user_playlist_add_tracks(userID, playlistID, playlistSongs)


def main(sp, user, model, mood):
    trackURIs, tracks = getUserTracks(sp)
    features = getAudioFeatures(sp, trackURIs)
    createPlaylist(sp, user, trackURIs, features, mood, model)
