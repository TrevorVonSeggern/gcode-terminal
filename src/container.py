from easy_inject import ServiceCollection
from settings import AllSettings
from service import ServiceA, ServiceB
from program import Program
from display.mainUi import MainUi

class Container:
    collection: ServiceCollection
    def __init__(self):
        collection = ServiceCollection()

        collection.registerInstance(AllSettings())

        collection.register(Program)
        collection.register(MainUi).singleton()

        self.collection = collection


