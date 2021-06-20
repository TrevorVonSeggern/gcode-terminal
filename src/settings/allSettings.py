from functools import cached_property
import json

class AllSettings:
    def __init__(self):
        self.configuration

    @cached_property
    def configuration(self):
        with open('appsettings.json', 'r') as f:
            return json.load(f)
