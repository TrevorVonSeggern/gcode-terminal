from functools import cached_property
import json
from service import *
from display import IMainUi

class Program:
    def __init__(self, ui: IMainUi):
        self.ui = ui

    @cached_property
    def configuration(self):
        with open('appsettings.json', 'r') as f:
            return json.load(f)

    def Run(self):
        print('run')

