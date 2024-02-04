import requests
import json
from collections import defaultdict
from dateutil import parser
from dateutil import tz

def convertTime(oldDate):
    pst_timezone = tz.gettz('America/Los_Angeles')
    parsed_datetime = parser.parse(oldDate)
    pst_datetime = parsed_datetime.astimezone(pst_timezone)
    return pst_datetime.strftime("%-I:%M %p")

r = requests.get('http://api.511.org/transit/StopMonitoring?agency=SF&api_key=c72ee226-6375-4071-a205-34bd469d6c57')
data=json.loads(r.text.encode().decode('utf-8-sig'))
stopIds = ["14869", "16017", "14303", "15186"]
listOfStops=data['ServiceDelivery']['StopMonitoringDelivery']['MonitoredStopVisit']
filteredStops = [{'busLine': x['MonitoredVehicleJourney']['LineRef'],
        'estimatedArrivalTime': x['MonitoredVehicleJourney']['MonitoredCall']['ExpectedArrivalTime'],
        'stopPointName': x['MonitoredVehicleJourney']['MonitoredCall']['StopPointName'],
        'stopId':x['MonitoringRef'] } for x in listOfStops if x['MonitoringRef'] in stopIds]
grouped_data = defaultdict(lambda: defaultdict(list))

for item in filteredStops:
    stop_id = item['stopId']
    bus_line = item['busLine']
    key = (stop_id, bus_line)
    grouped_data[key]['stopId'] = stop_id
    grouped_data[key]['stopPointName'] = item['stopPointName']
    grouped_data[key]['busLine'] = bus_line
    grouped_data[key]['estimatedArrivalTimes'].append(convertTime(item['estimatedArrivalTime']))

# Convert defaultdict to list of dictionary objects
formatted_data = []
for key, data in grouped_data.items():
    formatted_data.append({
        "stopId": data['stopId'],
        "stopPointName": data['stopPointName'],
        "busLine": data['busLine'],
        "estimatedArrivalTimes": data['estimatedArrivalTimes']
    })

sorted_data = sorted(formatted_data,key=lambda x: (x['busLine'], x['stopId']))

print(json.dumps(sorted_data))
