class IPMaker:
    def __init__(self):
        self.network_size = -1

    def get_address(self):
        self.network_size += 1
        return self.network_size
