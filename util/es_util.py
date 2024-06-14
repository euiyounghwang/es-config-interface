
import json

def json_read_config(path):
        ''' read config file with option'''
        with open(path, "r") as read_file:
            data = json.load(read_file)
        return data
    