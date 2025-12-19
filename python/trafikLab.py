import json
from os import getenv

import requests

resAPI = getenv("API_KEY")

def fetchStopId(name):
    response = requests.get("https://api.resrobot.se/v2.1/location.name?input=" + str(name) + "&maxNo=1&format=json&accessId=" + str(resAPI))
    data = json.loads(response.content)
    return data['stopLocationOrCoordLocation'][0]['StopLocation']['extId']

def findTrip(stop1, stop2):
    stopId1 = fetchStopId(stop1)
    stopId2 = fetchStopId(stop2)
    if stopId1 != -1 and stopId2 != -1:
        response = requests.get("https://api.resrobot.se/v2.1/trip?format=json&originId="
                                + str(stopId1) + "&destId="
                                + str(stopId2) +
                                "&numF=1&format=json&passlist=0&showPassingPoints=true&accessId="
                                + str(resAPI))
        data = json.loads(response.content)
        return readTrip(data)


def readTrip(jsonData):
    legs = jsonData['Trip'][0]['LegList']['Leg']
    legsOut = []

    for leg in legs:
        currentLeg = {
            "fromStation": leg['Origin']['name'],
            "fromTime": leg['Origin']['time'],
            "toStation": leg['Destination']['name'],
            "toTime": leg['Destination']['time'],
        }
        legsOut.append(currentLeg)

    return json.dumps(legsOut)


# for entity in feed.entity:
 #   if entity.HasField('trip_update'):
  #      print(entity.trip_update.stop_time_update)
