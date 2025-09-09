from astar import AStar



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
        # Manhatten distance
        return abs(n1[0] - n2[0]) + abs(n1[1] - n2[1])

    def heuristic_cost_estimate(self, current, goal):
        return 1

    def is_goal_reached(self, current, goal):
        return current[0] == goal[0]
