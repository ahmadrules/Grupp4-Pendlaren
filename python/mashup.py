import asyncio
import json
from datetime import datetime
import jsonpickle

from demolatar_api import DemolatarAPI
from trafiklab import fetchStopId, findTrip  # importera dina async-funktioner

# Om du vill räkna minuter från HH:MM:SS
def time_to_minutes(fromTime, toTime):
    f = datetime.strptime(fromTime, "%H:%M:%S")
    t = datetime.strptime(toTime, "%H:%M:%S")
    return int((t - f).total_seconds() / 60)

async def create_playlist_for_trip(start, destination, genre):
    # 1. Hämta trip från Trafiklab
    trip_json = await findTrip(start, destination)
    trip = jsonpickle.decode(trip_json)

    # 2. Räkna restid i minuter
    minutes_left = time_to_minutes(trip.fromTime, trip.toTime)

    # 3. Hämta spellista från Demolåtar
    demolatar = DemolatarAPI()
    playlist = demolatar.get_playlist_for_duration_and_genre(minutes_left, genre)

    # 4. Spara spellista till JSON
    trip_info = {
        "from": trip.fromStation,
        "to": trip.toStation,
        "departure": trip.fromTime,
        "arrival": trip.toTime,
        "travel_minutes": minutes_left
    }
    demolatar.save_playlist_to_json(playlist, filename="trip_playlist.json", genre=genre, trip_info=trip_info)

    return {
        "trip_info": trip_info,
        "genre": genre,
        "playlist": playlist
    }

# Kör test
if __name__ == "__main__":
    start_station = "Lund C"
    end_station = "Malmö C"
    genre = "rock"

    result = asyncio.run(create_playlist_for_trip(start_station, end_station, genre))
    print(json.dumps(result, indent=2, ensure_ascii=False))
