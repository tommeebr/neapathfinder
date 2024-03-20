import xml.etree.ElementTree as ET
import json
import os

def parse_osm(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()

    data = {}

    for node in root.findall('node'):
        id = node.get('id')
        lat = node.get('lat')
        lon = node.get('lon')

        data[id] = {
            'lat': float(lat),
            'lon': float(lon),
            'adj': []
        }

    for way in root.findall('way'):
        is_road = any(tag.get('k') == 'highway' for tag in way.findall('tag'))
        if is_road:
            nodes = [nd.get('ref') for nd in way.findall('nd')]
            for i in range(len(nodes) - 1):
                if nodes[i] in data and nodes[i + 1] in data:
                    data[nodes[i]]['adj'].append(nodes[i + 1])
                    data[nodes[i + 1]]['adj'].append(nodes[i])

    return data

def write_json(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# Get the directory of the script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to the OSM file
file_path = os.path.join(dir_path, 'attleborough.osm')

# Parse the OSM file
data = parse_osm(file_path)

# Construct the full path to the output JSON file
file_path_output = os.path.join(dir_path, 'attleborough.json')

# Write the data to the JSON file
write_json(data, file_path_output)