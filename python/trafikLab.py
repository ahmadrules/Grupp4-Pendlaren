import json
from os import getenv

import requests

resAPI = getenv("API_KEY")

def fetchStopId(name):
    response = requests.get("https://api.resrobot.se/v2.1/location.name?input=" + name + "&maxNo=1&format=json&accessId=" + resAPI)
    data = json.loads(response.content)
    return data['stopLocationOrCoordLocation'][0]['StopLocation']['extId']

def findTrip(stop1, stop2):
    response = requests.get("https://api.resrobot.se/v2.1/trip?format=json&originId="
                             + str(stop1) + "&destId="
                             + str(stop2) +
                             "&numF=1&format=json&passlist=0&showPassingPoints=true&accessId="
                             + resAPI)
    data = json.loads(response.content)
    return data


stopId1 = fetchStopId("MalmöRamelsVäg")
stopId2 = fetchStopId("Lund")

print(findTrip(stopId1, stopId2))

# for entity in feed.entity:
 #   if entity.HasField('trip_update'):
  #      print(entity.trip_update.stop_time_update)
