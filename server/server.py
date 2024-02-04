from flask import Flask
from flask import render_template
from flask_caching import Cache  # Import the caching library
import time  # For time-related functions
import requests
import json
from collections import defaultdict
from dateutil import parser
from dateutil import tz

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  # Simple in-memory cache

api_key="c72ee226-6375-4071-a205-34bd469d6c57"

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/updateData")
@cache.cached(timeout=90)  # Cache for 90 seconds (adjust as needed)
def updateData():
    current_time = time.time()
    cached_data = cache.get('bus_data')

    if cached_data and cached_data['timestamp'] + 90 > current_time:  # Check cache validity
        return cached_data['data']
    new_data = fetch_data_from_api()
    # Store new data in cache
    cache.set('bus_data', {'data': new_data, 'timestamp': current_time})

    return new_data

def convertTime(oldDate):
    pst_timezone = tz.gettz('America/Los_Angeles')
    parsed_datetime = parser.parse(oldDate)
    pst_datetime = parsed_datetime.astimezone(pst_timezone)
    return pst_datetime.strftime("%-I:%M %p")

def fetch_data_from_api():
    r = requests.get(f'http://api.511.org/transit/StopMonitoring?agency=SF&api_key={api_key}')
    decoded_data=r.text.encode().decode('utf-8-sig') 
    data = json.loads(decoded_data)
    desiredStopIds = ["14869", "16017", "14303", "15186", "16598", "15997"]

    allStops = data['ServiceDelivery']['StopMonitoringDelivery']['MonitoredStopVisit']

    filteredStops = [{'busLine': x['MonitoredVehicleJourney']['LineRef'],
            'estimatedArrivalTime': x['MonitoredVehicleJourney']['MonitoredCall']['ExpectedArrivalTime'],
            'stopPointName': x['MonitoredVehicleJourney']['MonitoredCall']['StopPointName'],
            'stopId': x['MonitoringRef'] 
            } for x in allStops if x['MonitoringRef'] in desiredStopIds]

    grouped_data = defaultdict(lambda: defaultdict(list))

    for item in filteredStops:
        stop_id = item['stopId']
        bus_line = item['busLine']
        key = (stop_id, bus_line)
        grouped_data[key]['stopId'] = stop_id
        grouped_data[key]['stopPointName'] = item['stopPointName']
        grouped_data[key]['busLine'] = bus_line
        grouped_data[key]['estimatedArrivalTimes'].append(item['estimatedArrivalTime'])

    # Convert defaultdict to list of dictionary objects
    formatted_data = []
    for key, data in grouped_data.items():
        formatted_data.append({
            "stopId": data['stopId'],
            "stopPointName": data['stopPointName'],
            "busLine": data['busLine'],
            "estimatedArrivalTimes": sorted(data['estimatedArrivalTimes'], reverse=False)
        })
    sorted_data = sorted(formatted_data, key=lambda x: (x['busLine'], x['stopId']))
    return sorted_data
