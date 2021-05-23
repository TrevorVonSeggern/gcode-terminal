from service import *

class Program:
    def __init__(self, a: ServiceA, b: ServiceB):
        self.a = a
        self.b = b

    def Run(self):
        print(self.a.color)
        print(self.b.color)
        print('run')

