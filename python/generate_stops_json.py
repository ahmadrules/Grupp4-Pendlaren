import csv
import json

INPUT_FILE = "data/stops.txt"
OUTPUT_FILE = "static/stops_skane.json"

stops = {}
# ^ dict istället för lista → automatiskt inga dubletter

with open(INPUT_FILE, encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        # 1️⃣ Vi vill bara ha "stationer"
        if row["location_type"] != "1":
            continue

        # 2️⃣ Hoppa över plattformar
        if row["parent_station"]:
            continue

        stop_id = row["stop_id"]
        stop_name = row["stop_name"]

        # 3️⃣ Undvik dubletter på namn
        if stop_name not in stops:
            stops[stop_name] = {
                "id": stop_id,
                "name": stop_name
            }

# Konvertera dict → lista
clean_stops = list(stops.values())

with open(OUTPUT_FILE, "w", encoding="utf-8") as jsonfile:
    json.dump(clean_stops, jsonfile, ensure_ascii=False, indent=2)

print(f"✅ Skapade {len(clean_stops)} UNIKA hållplatser i {OUTPUT_FILE}")
