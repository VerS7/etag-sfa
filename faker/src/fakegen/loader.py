"""
Data loader
"""
import json
import os


def get_files(directory: str, ext: str) -> list[str]:
    """Get all file paths by ext from directory"""
    files = []
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path) and full_path.endswith(ext):
            files.append(full_path)
        elif os.path.isdir(full_path):
            files.extend(get_files(full_path, ext))
    return files


def load_json(path: str) -> dict:
    """load json file to dict"""
    print(f"loading file: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return json.loads(file.read())


def load_all(directory: str) -> list[dict]:
    """load all json files from directory"""
    data = []
    files = get_files(directory=directory, ext=".json")
    for file in files:
        data.append(load_json(file))
    return data
