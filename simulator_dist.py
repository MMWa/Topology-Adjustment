import time
from random import randint

from forward_distributed_solution.ForwardDecentralizedSolution import ForwardDecentralizedSolution
from exhaustive_central_solution.ExhaustiveCentralSolution import ExhaustiveCentralSolution
from greedy_central_solution.GreedyCentralSolution import GreedyCentralSolution
from fui import WindowManager
from pursue_central_solution.PursueCentralSolution import PursueCentralSolution
from simulation.node import Node, Pos

if __name__ == "__main__":

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
    dist_list = ForwardDecentralizedSolution(40, node_list)
    greedy_list = GreedyCentralSolution(40, node_list)

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

        # print(dist_list.relay_list)

        game_window.greedy_relays = []
        for x in dist_list.relay_list[1:]:
            game_window.greedy_relays.append(x.position.as_int_array)

        for x in greedy_list.relay_list:
            game_window.pursue_relays.append(x.position.as_int_array)

        # call the tick/draw function
        game_window.tick(deltaT)

        # add random velocity onto the scenario, except to "base station"
        greedy_list.reset()

        event = game_window.catch_events()

        # print(event)

        if event == 119:
            # w
            node_list[1].position.velocity_add([0, move_coefficient])

        if event == 115:
            # s
            node_list[1].position.velocity_add([0, -move_coefficient])


        if event == 97:
            # a
            node_list[1].position.velocity_add([-move_coefficient, 0])


        if event == 100:
            # d
            node_list[1].position.velocity_add([move_coefficient, 0])

        if event == 92:
            print("Attempt to trigger Debugger")


        #node_list[1].position.velocity_add([randint(0, 2), randint(0, 2)])

        # reset the solution state
        # dist_list.reset()
