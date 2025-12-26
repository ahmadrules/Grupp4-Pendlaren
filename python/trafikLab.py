import json
from os import getenv
import Leg

import requests

resAPI = getenv("API_KEY")

def fetchStopId(name):
<<<<<<< Updated upstream
    response = requests.get("https://api.resrobot.se/v2.1/location.name?input=" + str(name) + "&maxNo=1&format=json&accessId=" + str(resAPI))
=======
    response = requests.get("https://api.resrobot.se/v2.1/location.name?input="
                            + name
                            + "&maxNo=1&format=json&accessId="
                            + resAPI)
>>>>>>> Stashed changes
    data = json.loads(response.content)
    return data['stopLocationOrCoordLocation'][0]['StopLocation']['extId']

def findTrip(stop1, stop2):
<<<<<<< Updated upstream
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
=======
    response = requests.get("https://api.resrobot.se/v2.1/trip?format=json&originId="
                             + str(stop1)
                             + "&destId="
                             + str(stop2) +
                             "&numF=1&format=json&passlist=0&showPassingPoints=true&accessId="
                             + resAPI)
    data = json.loads(response.content)
    getTripTime(data)
    getTripLegs(data)
    return data

def getTripTime(data):
    time = data['Trip'][0]['Origin']['time']
    time2 = data['Trip'][0]['Destination']['time']
    print(time)
    print(time2)
    h1, m1, s1 = time.split(':')
    h2, m2, s2 = time2.split(':')
    time1Sec = int(h1) * 3600 + int(m1) * 60 + int(s1)
    time2Sec = int(h2) * 3600 + int(m2) * 60 + int(s2)
    print((time2Sec - time1Sec)/60)
    return time2Sec - time1Sec

def getTripLegs(data):
    legs = []
    datalen = data['Trip'][0]['LegList']['Leg']
    for x in datalen:
        originName = x['Origin']['name']
        originTime = x['Origin']['time']
        destinationName = x['Destination']['name']
        destinationTime = x['Destination']['time']
        leg = Leg.Leg(originName, originTime, destinationName, destinationTime)
        print(leg.originName)
>>>>>>> Stashed changes

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
