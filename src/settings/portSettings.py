from allSettings import AllSettings

class PortSettings:
    def __init__(self, base: AllSettings):
        config = base.configuration
        self.fake = config['Fake'] if config['Fake'] == None else False
        self.port = config['Port'] if config['Port'] == None else '/dev/ttyUSB0'
        self.baud = config['Baud'] if config['Baud'] == None else 115200
