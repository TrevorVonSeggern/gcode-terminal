from easy_inject import ServiceCollection
from settings import AllSettings
from service import ServiceA, ServiceB
from program import Program

class Container:
    collection: ServiceCollection
    def __init__(self):
        collection = ServiceCollection()

        collection.registerInstance(AllSettings())

        collection.register(Program)
        collection.register(ServiceA)
        collection.register(ServiceB)

        self.collection = collection


