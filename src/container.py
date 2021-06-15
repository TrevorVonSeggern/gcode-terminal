from dependency_injection.ServiceCollection import ServiceCollection
from program import Program
from display.mainUi import MainUi

class Container:
    collection: ServiceCollection
    def __init__(self):
        collection = ServiceCollection()

        collection.register(Program)
        collection.register(MainUi).singleton()

        self.collection = collection


