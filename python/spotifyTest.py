import asyncio

import requests

async def getAuth():
    url = "https://accounts.spotify.com/api/token"
    data = {'grant_type' : 'client_credentials', 'client_id' : 'e6740bb7feb04f329db3f1cf4ebffefe', 'client_secret' : 'c33de715a721461c904836a34424c710'}
    r = requests.post(url, data=data)
    print(r.text)
    auth = r.json()['access_token']
    print(auth)
    return auth

async def getUserID():
    auth = await getAuth()
    url = "https://accounts.spotify.com/v1/me"
    headers = {'Authorization': 'Bearer ' + str(auth), "Content-Type": "application/json"}
    r = requests.get(url, headers=headers)
    print(r.text)


asyncio.run(getUserID())


