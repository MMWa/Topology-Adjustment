import random
from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm

from pursue_central_solution.PursueCentralSolution import PursueCentralSolution
from pursue_central_solution.PursueCentralSmarter import PursueCentralSmarterSolution
from greedy_central_solution.GreedyCentralSolution import GreedyCentralSolution

from decentralized_solution.DecentralizedNode import DecentralizedSolution
from decentralized_solution.DecentralizedNode import DecentralizedNode

from simulation.node import Node, Pos
from simulation.node.Node import NodeType

MAX_NODE_COUNT = 5
AVERAGE_SAMPLES = 10
UNIT_DISTANCE = 40
VELOCITY = 5


def area_shoelace(points):
    area = 0
    q = points[-1]
    for p in points:
        area += (p.position.x * q.position.y) - (p.position.y * q.position.x)
        q = p
    return area / 2


def total_distance_from_gateway(points : list[DecentralizedNode]):
    gateway = points[0]
    dist = 0
    for x in points[1:]:
        dist += gateway.distance_to(x)
    return dist

def avg_link_length(points: list[DecentralizedNode]):
    #points is the end node list
    link_acc = 0
    for x in points:
        if x.type == NodeType.End:
            link_acc =+ traverse_distance(x, 0)

def traverse_distance(point:DecentralizedNode, in_d):
    p = point.parent
    dist = in_d + point.distance_to(p)
    if p.type == NodeType.Home:
        return dist
    else:
        return traverse_distance(p, dist)

def total_distance_calc(relay_points, nodes, unit_distance):
    dist_ratio = len(relay_points)
    dist_ratio += len(nodes)
    return unit_distance * dist_ratio


if __name__ == "__main__":
    sample_size = [10,20,50]
    node_range = [5,10,15,20,25,30]

    for q in sample_size:
        AVERAGE_SAMPLES = q

        for w in node_range:
            MAX_NODE_COUNT = w
            nodes_list = []

            a_node = Node(Pos(0, 0))
            nodes_list.append(a_node)

            combined_simulator = []

            combined_simulator.append(DecentralizedSolution(UNIT_DISTANCE, nodes_list))

            nodes_list.append(DecentralizedNode(combined_simulator[3].sandbox, UNIT_DISTANCE, in_node=Node(Pos(10, 10))))
            combined_simulator[3].prepare()
            average_list = [np.zeros(len(combined_simulator))]

            for v in tqdm(range(MAX_NODE_COUNT)):
                value_list = []
                for _ in range(AVERAGE_SAMPLES):
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
                # pprint(average_list)
                tmp_node = DecentralizedNode(combined_simulator[3].sandbox, UNIT_DISTANCE, in_node=Node(Pos(0, 0)))
                tmp_node.type = NodeType.End
                tmp_node.parent = combined_simulator[3].relay_list[0]
                nodes_list.append(tmp_node)

            plt.plot(average_list)
            plt.grid(True)
            plt.legend(["Simple Pursue Algorithm", "Improved Pursue Algorithm", "Greedy Algorithm", "Decentralized Algorithm"])

            base_filename = "testdata/test_" + str(AVERAGE_SAMPLES) + "samples_" + str(MAX_NODE_COUNT) +"nodes"

            np.savetxt(base_filename+".csv", average_list, delimiter=",")
            plt.savefig(base_filename+".png")
            plt.clf()
            # plt.show()
