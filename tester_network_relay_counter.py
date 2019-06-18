import random
from pprint import pprint
from typing import List

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

MAX_NODE_COUNT = 30
AVERAGE_SAMPLES = 20
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


def multi_link(relays:List[Node], unit_dis, sim_type = None):
    multi_link_count = 0

    if sim_type == "cpD":
        for x in relays:
            if len(x.children) > 1:
                multi_link_count += 1

        return multi_link_count
    else:
        for x in relays :
            tmp_count = 0
            for y in relays:
                if x != y:
                    if x.type != NodeType.End:
                        if x.distance_to(y) <= unit_dis * 1:
                            tmp_count += 1
                            if tmp_count > 2:
                                multi_link_count += 1
        return multi_link_count

if __name__ == "__main__":
    nodes_list = []
    random.seed(9001)
    a_node = Node(Pos(0, 0))
    nodes_list.append(a_node)

    combined_simulator = []
    combined_simulator.append(PursueCentralSmarterSolution(UNIT_DISTANCE, nodes_list))
    combined_simulator.append(GreedyCentralSolution(UNIT_DISTANCE, nodes_list))
    combined_simulator.append(DecentralizedSolution(UNIT_DISTANCE, nodes_list))
    combined_simulator.append(PursueCentralSolution(UNIT_DISTANCE, nodes_list))


    nodes_list.append(DecentralizedNode(combined_simulator[2].sandbox, UNIT_DISTANCE, in_node=Node(Pos(10, 10))))
    combined_simulator[2].prepare()
    average_list = [np.zeros(len(combined_simulator))]

    for v in tqdm(range(MAX_NODE_COUNT)):
        value_list = []
        for _ in range(AVERAGE_SAMPLES):
            for x in nodes_list[1:]:
                x.position.velocity_add([random.randint(-VELOCITY, VELOCITY), random.randint(-VELOCITY, VELOCITY)])

            print_list = []
            for idx, x in enumerate(combined_simulator[:4]):
                if idx == 2:
                    for _ in range(30):
                        x.execute_pipeline()
                    print_list.append(len(x.relay_list))
                else:

                    x.execute_pipeline()
                    print_list.append(len(x.relay_list))
                    x.reset()
        #
            value_list.append(print_list)
            # pprint(value_list)
        average_list.append(np.mean(value_list, axis=0))
        # pprint(average_list)
        tmp_node = DecentralizedNode(combined_simulator[2].sandbox, UNIT_DISTANCE, in_node=Node(Pos(0, 0)))
        tmp_node.type = NodeType.End
        tmp_node.parent = combined_simulator[2].relay_list[0]
        nodes_list.append(tmp_node)

    # pprint(average_list)
    plt.plot(average_list)
    plt.grid(True)
    plt.legend(["Improved Pursue Algorithm", "Greedy Algorithm", "Decentralized Algorithm", "Simple Pursue Algorithm"])
    plt.xlabel("Number of Nodes")
    plt.ylabel("Number of Relays")
    plt.show()
    #
    # base_filename = "testdata2/test_" + str(AVERAGE_SAMPLES) + "samples_" + str(MAX_NODE_COUNT) + "nodes"
    #
    # np.savetxt(base_filename + ".csv", average_list, delimiter=",")
    # plt.savefig(base_filename + ".png")
    # plt.clf()
    #
    # # pprint(np.sum(average_list, axis=1))
    # dif_list = []
    # for x in average_list:
    #     dif_list.append(np.divide(x[0], x[1]))
    #
    # plt.plot(dif_list)
    # plt.grid(True)
    # plt.legend(["Distance Approximation", "True Distance"])
    # plt.xlabel("Number of Nodes")
    #
    #
    # base_filename = "testdata2/test3_" + str(AVERAGE_SAMPLES) + "samples_" + str(MAX_NODE_COUNT) + "nodes"
    # np.savetxt(base_filename + ".csv", dif_list, delimiter=",")
    # plt.savefig(base_filename + ".png")
    # plt.clf()
