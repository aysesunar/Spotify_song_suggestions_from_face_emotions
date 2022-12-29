import pandas
import time
import csv


def searchForTracks(sp):
    dataset = pandas.read_csv("tagMoods.csv")
    tracks = []
    tracksForData = []
    for i in range(len(dataset['title'])):
        title = dataset['title'][i]
        results = sp.search(q='track:' + title, type='track')
        time.sleep(1)
        items = results['tracks']['items']
        if len(items) > 0:
            if items[0]['artists'][0]['name'] == dataset['artist'][i]:
                tracks.append(items[0]['id'])
                tracksForData.append([items[0]['id'], dataset['mood'][i]])
    with open('tracksInSpotify.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(tracksForData)):
            line = [tracksForData[i]]
            writer.writerow(line)


def getAudioFeatures(sp):
    dataset = pandas.read_csv("tracksInSpotify.csv")
    dataset = pandas.Series.tolist(dataset)
    tracks = []
    data = []
    for elem in dataset:
        res = elem[0].strip('][').replace("'", "").split(', ')
        data.append(res)
        tracks.append(res[0])

    features = []
    featuresTotal = []
    max = 100
    for i in range(0, len(tracks), max):
        audioFeatures = sp.audio_features(tracks[i:i + max])
        time.sleep(1)
        for j in range(len(audioFeatures)):
            if (audioFeatures != None):
                features.append(audioFeatures[j]['danceability'])
                features.append(audioFeatures[j]['energy'])
                features.append(audioFeatures[j]['valence'])
                featuresTotal.append(features)
            features = []
    return data, featuresTotal


def writeToCSV(data, features):
    with open('songMoods.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(features)):
            line = [data[i][0]] + features[i] + [data[i][1]]
            writer.writerow(line)


def main(sp):
    searchForTracks(sp)
    data, features = getAudioFeatures(sp)
    writeToCSV(data, features)
