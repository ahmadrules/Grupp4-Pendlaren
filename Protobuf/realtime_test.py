import gtfs_realtime_pb2
import csv

#realtime för skåne
realtime_file = "data/TripUpdates.pb"

feed = gtfs_realtime_pb2.FeedMessage()
with open(realtime_file, "rb") as f:
    feed.ParseFromString(f.read())

print("Antal entities (Realtime):", len(feed.entity))

#static
stops_file = "data/skane/skane/stops.txt"

with open(stops_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i == 5:
            break
        print(row["stop_id"], "-", row["stop_name"])
