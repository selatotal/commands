import json


class Config:

    cfg = {}

    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.cfg = json.load(file)
