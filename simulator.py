import time
from random import randint

from exhaustive_central_solution.ExhaustiveCentralSolution import ExhaustiveCentralSolution
from greedy_central_solution.GreedyCentralSolution import GreedyCentralSolution
from fui import WindowManager
from pursue_central_solution.PursueCentralSolution import PursueCentralSolution
from simulation.node import Node, Pos

if __name__ == "__main__":

    # create a list of nodes, this is our scenario
    node_list = []
    node_list.append(Node(Pos(0, 0)))
    node_list.append(Node(Pos(10 * 10, 11 * 10)))
    node_list.append(Node(Pos(9 * 10, 20 * 10)))
    node_list.append(Node(Pos(25 * 10, 18 * 10)))
    node_list.append(Node(Pos(2 * 10, 15 * 10)))
    node_list.append(Node(Pos(18 * 10, -5 * 10)))
    node_list.append(Node(Pos(25 * 10, 25 * 10)))
    node_list.append(Node(Pos(-5 * 10, 25 * 10)))

    # shove the list into a scenario solver
    greedy_list = GreedyCentralSolution(20, node_list)
    pursue_list = PursueCentralSolution(20, node_list)
    exhaustive_list = ExhaustiveCentralSolution(20, node_list)
    game_window = WindowManager()

    while True:
        # execute the scenario solver
        deltaT = time.time()
        greedy_list.execute_pipeline()
        pursue_list.execute_pipeline()
        deltaT = time.time() - deltaT

        # take the solutions into the window rendered
        for x in node_list:
            game_window.nodes.append(x.position.as_int_array)

        for x in greedy_list.relay_list:
            game_window.greedy_relays.append(x.position.as_int_array)

        for x in pursue_list.relay_list:
            game_window.pursue_relays.append(x.position.as_int_array)

        # call the tick/draw function
        game_window.tick(deltaT)

        # add random velocity onto the scenario, except to "base station"
        for x in node_list[1:]:
            x.position.velocity_add([randint(-4, 4), randint(-4, 4)])

        # reset the solution state
        greedy_list.reset()
        pursue_list.reset()
