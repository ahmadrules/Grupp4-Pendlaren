import json
from google.transit import gtfs_realtime_pb2
import requests

#feed = gtfs_realtime_pb2.FeedMessage()
#response = requests.get("https://opendata.samtrafiken.se/gtfs-rt/skane/TripUpdates.pb?key=362642b3454f4932886d717537c14846")

#feed.ParseFromString(response.content)
#print(feed.entity[0].trip_update.stop_time_update[0].arrival.delay)

resAPI = "b33ebb15-55e2-4b01-a3ed-391ef83278cd"

def fetchStopId(name):
    response = requests.get("https://api.resrobot.se/v2.1/location.name?input=" + name + "&maxNo=1&format=json&accessId=" + resAPI)
    data = json.loads(response.content)
    return data['stopLocationOrCoordLocation'][0]['StopLocation']['extId']

def findTripId(stop1, stop2):
    response = requests.get("https://api.resrobot.se/v2.1/trip?format=json&originId="
                             + str(stop1) + "&destId="
                             + str(stop2) +
                             "&numF=1&format=json&passlist=0&showPassingPoints=true&accessId="
                             + resAPI)
    data = json.loads(response.content)


# for entity in feed.entity:
 #   if entity.HasField('trip_update'):
  #      print(entity.trip_update.stop_time_update)
