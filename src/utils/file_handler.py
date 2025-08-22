import os
import json

def ensure_directory_exists(directory_path):
    """Ensure that a directory exists, create it if it doesn't"""
    if directory_path and not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")

def load_json_file(file_path):
    """Load JSON file and return the data"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from {file_path}: {e}")
        return None

def save_json_file(data, file_path):
    """Save data to JSON file"""
    try:
        ensure_directory_exists(os.path.dirname(file_path))
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data saved to: {file_path}")
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")