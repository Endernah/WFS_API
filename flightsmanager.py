import json

def createFlight(callsign, time, aircraft):
    with open('flights.json', 'r') as f:
        flights = json.load(f)

    # Add new flight
    flights[callsign] = {
        "time": time,
        "aircraft": aircraft
    }
    with open('flights.json', 'w') as f:
        json.dump(flights, f)
    return flights

def getFlights():
    with open('flights.json', 'r') as f:
        data = json.load(f)
    return data

def getFlight(callsign):
    with open('flights.json', 'r') as f:
        data = json.load(f)
    if callsign in data:
        return data[callsign]
    else:
        return "Flight not found."

def deleteFlight(callsign):
    with open('flights.json', 'r') as f:
        data = json.load(f)
    if callsign in data:
        del data[callsign]
        with open('flights.json', 'w') as f:
            json.dump(data, f)
        return "Flight deleted."
    else:
        return "Flight not found."