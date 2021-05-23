from dependency_injection.ServiceCollection import ServiceCollection
from service import ServiceA, ServiceB
from program import Program

class Container:
    collection: ServiceCollection
    def __init__(self):
        collection = ServiceCollection()

        collection.register(Program)
        collection.register(ServiceA)
        collection.register(ServiceB)

        self.collection = collection


