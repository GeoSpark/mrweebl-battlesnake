from astar import AStar

from utils import manhattan_distance

BOARD_WEIGHT_EMPTY = 1
BOARD_WEIGHT_FOOD = 1
BOARD_WEIGHT_SNAKE = 100
BOARD_WEIGHT_HAZARD = 100
BOARD_WEIGHT_SNAKE_HALO = 30


class SnakeAStar(AStar):
    def __init__(self, nodes):
        self.nodes = nodes

    def neighbors(self, n):
        for n1 in self.nodes[n]:
            yield n1

    def distance_between(self, n1, n2):
        return 1

    def heuristic_cost_estimate(self, current, goal) -> float:
        return manhattan_distance(current, goal)

    def is_goal_reached(self, current, goal):
        return current == goal
