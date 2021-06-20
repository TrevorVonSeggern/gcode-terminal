from functools import cached_property
import json
from service import *

class Program:
    def __init__(self, a: ServiceA, b: ServiceB):
        self.a = a
        self.b = b

    @cached_property
    def configuration(self):
        with open('appsettings.json', 'r') as f:
            return json.load(f)

    def Run(self):
        print(self.a.color)
        print(self.b.color)
        print('run')

