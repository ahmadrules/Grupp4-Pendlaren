from flask import Flask, request, make_response, jsonify
import asyncio
import json
import jsonpickle
from datetime import datetime

from demolatar_api import DemolatarAPI
from trafiklab import fetchStopId, findTrip  # dina async-funktioner

app = Flask(__name__)

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

    # Skapa trip-info
    trip_info = {
        "from": trip.fromStation,
        "to": trip.toStation,
        "departure": trip.fromTime,
        "arrival": trip.toTime,
        "travel_minutes": minutes_left
    }

    return {
        "trip_info": trip_info,
        "genre": genre,
        "playlist": playlist
    }

# Flask-route som sätter spellistan i cookie
@app.route("/trip_playlist")
def trip_playlist():
    start = request.args.get("start", "Lund C")
    destination = request.args.get("destination", "Malmö C")
    genre = request.args.get("genre", "rock")

    # Kör async-funktionen
    result = asyncio.run(create_playlist_for_trip(start, destination, genre))

    # Sätt spellistan i cookie
    playlist_json = json.dumps(result["playlist"])
    resp = make_response(jsonify(result))
    resp.set_cookie("playlist", playlist_json, max_age=3600, httponly=True)  # 1 timme

    return resp

if __name__ == "__main__":
    app.run(debug=True)
