import time
from pygame.constants import *

from forward_distributed_solution.MultiForwardDecentralizedSolution import MultiForwardDecentralizedSolution
from greedy_central_solution import GreedyCentralSolution
from fui import WindowManager
from simulation.node import Node, Pos
from simulation.node.Node import NodeType

if __name__ == "__main__":
    node_selector = 1

    move_coefficient = 10

    # create a list of nodes, this is our scenario
    node_list = []
    a_node = Node(Pos(0, 0))
    b_node = Node(Pos(1.7*10, 1*10))
    c_node = Node(Pos(2*10, 2*10))

    node_list.append(a_node)
    node_list.append(b_node)
    #node_list.append(c_node)

    # shove the list into a scenario solver
    dist_list = MultiForwardDecentralizedSolution(40, node_list)
    greedy_list = GreedyCentralSolution(40*.8, node_list)

    game_window = WindowManager()


    while True:

        # execute the scenario solver
        deltaT = time.time()
        dist_list.execute_pipeline()
        greedy_list.execute_pipeline()
        deltaT = time.time() - deltaT

        # take the solutions into the window rendered
        for x in node_list:
            game_window.nodes.append(x.position.as_int_array)

        game_window.greedy_relays = []
        for x in dist_list.relay_list[1:]:
            game_window.greedy_relays.append(x.position.as_int_array)

        for x in greedy_list.relay_list:
            game_window.pursue_relays.append(x.position.as_int_array)

        game_window.selection = node_list[node_selector].position.as_int_array


        # call the tick/draw function
        game_window.tick(deltaT)

        # add random velocity onto the scenario, except to "base station"
        greedy_list.reset()

        event = game_window.catch_events()

        if event == K_w:
            node_list[node_selector].position.velocity_add([0, move_coefficient])
        if event == K_s:
            node_list[node_selector].position.velocity_add([0, -move_coefficient])
        if event == K_a:
            node_list[node_selector].position.velocity_add([-move_coefficient, 0])
        if event == K_d:
            node_list[node_selector].position.velocity_add([move_coefficient, 0])
        if event == 92:
            print("Attempt to trigger Debugger")

        if event == K_o:
            to_add = Node(Pos(0, 0))
            to_add.type = NodeType.End
            node_list.append(to_add)

        if event == K_p:
            node_selector += 1
            if node_selector == len(node_list):
                node_selector = 1

        # node_list[1].position.velocity_add([randint(0, 2), randint(0, 2)])