import math

import numpy as np


class PropagationModel():
    def __init__(self, noise=2):
        self._noise = noise

    def get_noise(self):
        mu, sigma = 0, 0.1  # mean and standard deviation
        return self._noise + np.random.normal(mu, sigma)

    def get_receiver_power(self, node, x, transmission_power):
        # find the transmission distance
        distance = math.sqrt(((x[0] - node[0]) ** 2) + ((x[1] - node[1]) ** 2))
        distance = abs(distance)

        try:
            signal = 10 * math.log10(transmission_power / (distance ** 2))
            # (signal - (10 * math.log10(self.get_noise()))) can be done later, adding noise
            # but it has to be compensated for at the receiving side
            # because the distance re-estimation will be off
            return signal
        except ValueError:
            return 10 * math.log10(self.get_noise())

        except ZeroDivisionError:
            return 0


if __name__ == "__main__":
    prop = PropagationModel()
    oneNode = [0, 0]
    dest = [0, 10]
    result = prop.get_receiver_power(oneNode, dest, 0.5)
    print(str(result))
