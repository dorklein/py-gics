import json

from gics.map import Map


def json_to_map(path: str) -> Map:
    with open(path, 'r') as f:
        data = json.load(f)

    return Map.create_recursively(data)
