from display import IMainUi

class Program:
    def __init__(self, ui: IMainUi):
        self.ui = ui

    def Run(self):
        print('run')

