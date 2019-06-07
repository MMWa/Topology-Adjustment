from simulation.node import Node


class ProtoNode(Node):
    def __init__(self, environment, unit_distance, position=None, in_node=None, parent=None):
        self.parent = parent
        self.children = []

        self.unit_distance = unit_distance
        self.critical_range = self.unit_distance
        self.safe_range = self.unit_distance * 0.8

        if in_node is not None:
            super().__init__(in_node.position)
        elif position is not None:
            super().__init__(position)
        else:
            super().__init__()

    def tell(self, dest, data):

if __name__ == "__main__":
