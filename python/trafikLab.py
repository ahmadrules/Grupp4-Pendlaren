import json
from datetime import datetime
from itertools import product

from humanfriendly import format_timespan
import jsonpickle
import requests
from Leg import Leg
from Trip import Trip

file = open("keys/TRAFIKLAB_KEY.txt")
resAPI = file.read()

async def fetchStopId(name):
    link = "https://api.resrobot.se/v2.1/location.name?input=" + str(name) + "&maxNo=1&format=json&accessId=" + str(resAPI)
    response = requests.get(link)
    data = json.loads(response.content)

    items = data.get("stopLocationOrCoordLocation", [])
    if not items:
        return -1
    
    for item in items:
        if "StopLocation" in item and "extId" in item["StopLocation"]:
            return item["StopLocation"]["extId"]
        
    for item in items:
        if "CoordLocation" in item and "extId" in item["CoordLocation"]:
            return item["CoordLocation"]["extId"]
        
    return -1
    
    
    #return data['stopLocationOrCoordLocation'][0]['StopLocation']['extId']

async def findTrip(stop1, stop2):
    stopId1 = await fetchStopId(stop1)
    stopId2 = await fetchStopId(stop2)
    if stopId1 != -1 and stopId2 != -1:
        response = requests.get("https://api.resrobot.se/v2.1/trip?format=json&originId="
                                + str(stopId1) + "&destId="
                                + str(stopId2) +
                                "&numF=1&format=json&passlist=0&showPassingPoints=true&accessId="
                                + resAPI)

        data = json.loads(response.content)
        #print(data)
        return readTrip(data)

def readTrip(jsonData):
    legs = jsonData['Trip'][0]['LegList']['Leg']
    legsOut = []

    for leg in legs:
        fromStation = leg['Origin']['name']
        fromTime = leg['Origin']['time']
        toStation = leg['Destination']['name']
        toTime = leg['Destination']['time']

        totalTime = format_timespan(calculateTime(fromTime, toTime))

        modeOfTravel = readModeOfTravel(leg)

        leg = Leg(fromStation, fromTime, toStation, toTime, totalTime, modeOfTravel[0], modeOfTravel[1])
        legsOut.append(leg)

    fromStation = jsonData['Trip'][0]['Origin']['name']
    toStation = jsonData['Trip'][0]['Destination']['name']
    fromTime = jsonData['Trip'][0]['Origin']['time']
    toTime = jsonData['Trip'][0]['Destination']['time']

    totalSeconds = calculateTime(fromTime, toTime)
    totalTime = format_timespan(totalSeconds)

    trip = Trip(fromStation, fromTime, toStation, toTime, totalTime, totalSeconds, legsOut)

    print(jsonpickle.encode(trip))
    return trip

def calculateTime(fromTime, toTime):
    fDate = datetime.strptime(fromTime, "%H:%M:%S")
    tDate = datetime.strptime(toTime, "%H:%M:%S")
    difference = tDate - fDate
    differenceStr = difference.total_seconds()
    return differenceStr

def readModeOfTravel(jsonData):
    product = jsonData['Product'][0]['name']

    if product is None:
        product = jsonData['Notes']['Note'][0]['value']

    if product == 'Promenad':
        return ['Promenad', '0']

    if product.find('Länstrafik - Buss') != -1:
        line = int(product.replace('Länstrafik - Buss ', ''))

        if line < 100:
            return ['Stadsbuss', line]
        else:
            return ['Regionbuss', line]

    if product.find("Regional") != -1:
        line = int(product.replace('Regional Tåg ', ''))
        return ['Öresundståg', line]
    else:
        line = int(product.replace('Länstrafik - Tåg ', ''))
        return ['Pågatåg', line]
    
def _as_list(x):
    if x is None:
        return []
    return x if isinstance(x, list) else [x]

async def findRouteStops(stop1, stop2):
    stopId1 = await fetchStopId(stop1)
    stopId2 = await fetchStopId(stop2)

    if stopId1 != -1 and stopId2 != -1:
        response = requests.get(
            "https://api.resbot.se/v2.1/trip?format=json&originId="
            + str(stopId1) + "&destId="
            + str(stopId2) +
            "&numF=1&format=json&passlist=1&showPassingPoints=true&accessId="
            + resAPI
        )
        data = json.loads(response.content)

        legs = data['Trip'][0]['LegList']['Leg']
        route = []
        seen = set()

        for leg in legs:
            stops_block = leg.get("Stops", {}).get("Stop")

            stops = []
            for s in _as_list(stops_block):
                name = s.get("name")
                if name:
                    stops.append(name)

            # Om det ej finns några stopp längst rutten
            if not stops:
                stops = [leg["Origin"]["name"], leg ["Destination"]["name"]]

            for name in stops:
                key = name.strip().lower()
                if not route or route[-1] != name:
                    if key not in seen:
                        route.append(name)
                        seen.add(key)

            return route
        
        return []