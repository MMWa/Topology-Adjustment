import random
from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from tqdm import tqdm

from pursue_central_solution.PursueCentralSolution import PursueCentralSolution
from pursue_central_solution.PursueCentralSmarter import PursueCentralSmarterSolution
from greedy_central_solution.GreedyCentralSolution import GreedyCentralSolution

from decentralized_solution.DecentralizedNode import DecentralizedSolution
from decentralized_solution.DecentralizedNode import DecentralizedNode

from simulation.node import Node, Pos
from simulation.node.Node import NodeType

MAX_NODE_COUNT = 30
UNIT_DISTANCE = 40
VELOCITY = 5


def area_shoelace(points):
    area = 0
    q = points[-1]
    for p in points:
        area += (p.position.x * q.position.y) - (p.position.y * q.position.x)
        q = p
    return area / 2


def total_distance_from_gateway(points):
    gateway = points[0]
    dist = 0
    for x in points[1:]:
        dist += gateway.distance_to(x)
    return dist


def total_distance_calc(relay_points, nodes, unit_distance):
    dist_ratio = len(relay_points)
    dist_ratio += len(nodes)
    return unit_distance * dist_ratio


if __name__ == "__main__":
    nodes_list = []

    a_node = Node(Pos(0, 0))
    nodes_list.append(a_node)

    combined_simulator = []
    combined_simulator.append(PursueCentralSolution(UNIT_DISTANCE, nodes_list))
    combined_simulator.append(PursueCentralSmarterSolution(UNIT_DISTANCE, nodes_list))
    combined_simulator.append(GreedyCentralSolution(UNIT_DISTANCE, nodes_list))
    combined_simulator.append(DecentralizedSolution(UNIT_DISTANCE, nodes_list))

    nodes_list.append(DecentralizedNode(combined_simulator[3].sandbox, UNIT_DISTANCE, in_node=Node(Pos(10, 10))))
    combined_simulator[3].prepare()
    print(combined_simulator[3].relay_list)
    average_list = [np.zeros(len(combined_simulator))]

    for v in tqdm(range(MAX_NODE_COUNT)):
        value_list = []
        for _ in range(50):
            for x in nodes_list[1:]:
                x.position.velocity_add([random.randint(-VELOCITY, VELOCITY), random.randint(-VELOCITY, VELOCITY)])

            print_list = []
            for idx, x in enumerate(combined_simulator[:4]):
                if idx == 3:
                    for _ in range(30):
                        x.execute_pipeline()
                    print_list.append(total_distance_calc(x.relay_list, nodes_list[1:], UNIT_DISTANCE))
                else:
                    x.execute_pipeline()
                    print_list.append(total_distance_calc(x.relay_list, nodes_list[1:], UNIT_DISTANCE))
                    x.reset()
            value_list.append(print_list)
        average_list.append(np.mean(value_list, axis=0))
        pprint(average_list)
        tmp_node = DecentralizedNode(combined_simulator[3].sandbox, UNIT_DISTANCE, in_node=Node(Pos(0, 0)))
        tmp_node.type = NodeType.End
        # print(combined_simulator[3].relay_list)
        tmp_node.parent = combined_simulator[3].relay_list[0]
        nodes_list.append(tmp_node)

    # np.savetxt("average_list.csv", average_list, delimiter=",")
    plt.plot(average_list)
    plt.grid(True)
    plt.legend(["Simple Pursue Algorithm", "Improved Pursue Algorithm", "Greedy Algorithm", "Decentralized Algorithm"])

    plt.show()

    combined_simulator_decentralized = []
    pos_list = []
