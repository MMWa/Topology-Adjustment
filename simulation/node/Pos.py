import random


class Pos:
    def __init__(self, x=None, y=None):
        if x is None:
            self.x = random.uniform(0, 50)
        else:
            self.x = x

        if y is None:
            self.y = random.uniform(0, 50)
        else:
            self.y = y

    def velocity_add(self, vector):
        self.x += vector[0]
        self.y += vector[1]

    @property
    def as_array(self):
        return [self.x, self.y]

    @property
    def as_int_array(self):
        return [int(self.x), int(self.y)]
