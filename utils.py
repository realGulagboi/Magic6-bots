import json
import os

settings_file = 'bot_settings.json'

# Load settings from JSON File
def load_settings():    
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            return json.load(f)
    return {}

# Save settings to JSOn File
def save_settings(settings):
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=4)