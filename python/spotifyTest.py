import asyncio
import base64
from dataclasses import replace

import requests

file = open("keys/SPOTIFY_SECRET.txt")
client_secret = file.read()
client_id = 'e6740bb7feb04f329db3f1cf4ebffefe'

async def getAccessToken(auth):
    authCC = client_id + ':' + client_secret

    authbytes = authCC.encode("utf-8")
    base64bytes= base64.b64encode(authbytes)
    base64string = base64bytes.decode("utf-8")

    auth64 = 'Basic ' + base64string

    # HÄR HÄMTAS ACCESS_TOKEN
    url = "https://accounts.spotify.com/api/token"
    data = {'grant_type' : 'authorization_code', 'code' : auth, 'redirect_uri' : 'https://127.0.0.1:8000/callback'}
    headers = {'Authorization': str(auth64), "Content-Type": "application/x-www-form-urlencoded"}

    r = requests.post(url, data= data, headers=headers)
    if r.status_code != 200:
        print("COULDNT FIND ACCESS TOKEN")
        print("ERROR MESSAGE: " + r.reason)
        print(r.text)
    else:
        print(">>>FOUND ACCESS TOKEN")
        return r.json()['access_token']



async def getUserID():
    url = "https://api.spotify.com/v1/me"
    file = open("keys/SPOTIFY_ACCESS_TOKEN.txt")
    access_token =  file.read()
    headers = {'Authorization': 'Bearer ' + access_token}

    # HÄR HÄMTAS USER_ID
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print(">>>USER ID")
        with open("keys/SPOTIFY_USER_ID.txt", "w") as f:
            f.write(r.json()['id'])
        return r.json()['id']

async def searchForTracks(genre):
    q = 'q=remaster%2520genre%3A'+ genre + '&type=track&market=SE&limit=50'
    url = "https://api.spotify.com/v1/search?" + q
    file = open("keys/SPOTIFY_ACCESS_TOKEN.txt")
    access_token =  file.read()

    headers = {"Authorization" : 'Bearer ' + str(access_token)}
    r = requests.get(url, headers=headers)
    tracks = []

    if r.status_code == 200:
        print(">>>FOUND TRACKS")
        for track in r.json()['tracks']['items']:
            data = {"uri": track['uri'], "track_duration" : track['duration_ms']}
            tracks.append(data)

        return tracks

    else:
        print("ERROR LOADING TRACKS")

async def createPlaylist():
    await getUserID()

    auth = open("keys/SPOTIFY_ACCESS_TOKEN.txt").read()
    userID = open( "keys/SPOTIFY_USER_ID.txt").read()

    url = "https://api.spotify.com/v1/users/" + userID + "/playlists"
    headers = {'Authorization': 'Bearer ' + auth, 'Content-Type': 'application/json'}
    data = {"name" : "Stinas lista", "description" : "Testar API snälla funka"}

    p = requests.post(url, headers=headers, json=data)
    if p.status_code == 201:
        print(">>>CREATED PLAYLIST")
        playlistID = p.json()['id']
        print(playlistID)

        return playlistID
    else:
        print("ERROR CREATING PLAYLIST")

async def getLatestCreatedPlaylist():
    userID = getUserID()
    auth = open("keys/SPOTIFY_ACCESS_TOKEN.txt").read()

    url = "https://api.spotify.com/v1/users/" + userID + "/playlists"
    headers = {'Authorization': 'Bearer ' + auth, 'Content-Type': 'application/json'}

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print(">>>FOUND PLAYLIST")
        return r.json()['items'][0]

async def fillPlaylist(genre, length):
    auth = open("keys/SPOTIFY_ACCESS_TOKEN.txt").read()
    playlistID = await createPlaylist()
    tracks = await searchForTracks(genre)

    uris = []
    totalPlaylistLength = 0
    for track in tracks:
        data = track['uri']
        totalPlaylistLength = totalPlaylistLength + int(track['track_duration'])
        uris.append(data)
        if totalPlaylistLength/1000 >= length:
            totalSeconds = totalPlaylistLength/1000
            print(">>>TOTAL AMOUNT OF TRACKS " + str(len(uris)))
            print(">>>TOTAL DURATION " + str(totalSeconds/60))
            break

    url = "https://api.spotify.com/v1/playlists/" + playlistID + "/tracks"
    headers = {'Authorization': 'Bearer ' + auth, 'Content-Type': 'application/json'}
    data = {'uris' : uris}

    p = requests.post(url, headers=headers, json=data)
    if p.status_code == 201:
        print(">>>FILLED PLAYLIST")
        latestPlaylist = await getLatestCreatedPlaylist()
        image = latestPlaylist['images'][0]['url']
        url = latestPlaylist['external_urls']['spotify']
        return {'image' : image, 'url' : url}
    else:
        print("ERROR FILLing PLAYLIST")











