import numpy as np
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm

def give_coords(source, dest):
    # Specify the coordinates (longitude, latitude) of origin and destination
    # first parameter is longitude, second parameter is latitude

    # Get geo nodes for the given source and destination points
    start = "{},{}".format(source[0], source[1])
    end = "{},{}".format(dest[0], dest[1])

    # Service - 'route', mode of transportation - 'driving', without alternatives
    url = 'http://router.project-osrm.org/route/v1/driving/{};{}?alternatives=false&annotations=nodes'.format(start, end)

    headers = {'Content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    print("Calling API ...:", r.status_code)  # Status Code 200 is success

    try:
        routejson = r.json()
        # Choose an alternative route if available
        if 'routes' in routejson and len(routejson['routes']) > 0:
            route_nodes = routejson['routes'][0]['legs'][0]['annotation']['nodes']
        else:
            raise ValueError("No valid routes found.")
    except ValueError as e:
        print("Error parsing JSON response:", e)
        print("Response content:", r.text)
        route_nodes = []

    # Keep every third element in the node list to optimize time
    route_list = [node for i, node in enumerate(route_nodes) if i % 3 == 1]

    coordinates = []

    for node in tqdm(route_list):
        try:
            url = 'https://api.openstreetmap.org/api/0.6/node/' + str(node)
            r = requests.get(url, headers=headers)
            myroot = ET.fromstring(r.text)
            for child in myroot:
                lat, lon = float(child.attrib['lat']), float(child.attrib['lon'])
            coordinates.append((lat, lon))
        except:
            continue

    return coordinates

# List of bus stops and their coordinates
bus_stops = [
    ('ZOB', (11.4232, 48.7689)),
    ('Harderstraße', (11.4318, 48.7657)),
    ('Auf der Schanz', (11.4301, 48.7637)),
    ('Universität (Kreuztor)', (11.4259, 48.7651)),
    ('Taschenturm', (11.4205, 48.7634)),
    ('Christoph-Scheiner-Gymnasium', (11.4221, 48.7640)),
    ('Rathausplatz', (11.4256, 48.7641)),
    ('Brückenkopf', (11.4334, 48.7632)),
    ('Schulzentrum SW, Gustav-Adolf-Weningstraße', (11.4167, 48.7592)),
    ('Feselenstraße', (11.4135, 48.7573)),
    ('Buchnerstraße', (11.4197, 48.7584)),
    ('Schröplerstraße', (11.4242, 48.7577)),
    ('Tassilostraße', (11.4289, 48.7573)),
    ('Erletstraße', (11.4330, 48.7582)),
    ('Canisiusstraße', (11.4381, 48.7599)),
    ('Frueaufstraße', (11.4402, 48.7608)),
    ('Martin-Hemm-Straße', (11.4432, 48.7618))
    # Add more bus stops if you NEEEDD BROO!!
]

# Initialize the list to store all coordinates
all_coordinates = []

# Iterate over bus stops
for i in range(len(bus_stops) - 1):
    source = bus_stops[i][1]
    dest = bus_stops[i + 1][1]
    coordinates = give_coords(source, dest)
    all_coordinates.extend(coordinates)

# Print all coordinates
print(all_coordinates)
