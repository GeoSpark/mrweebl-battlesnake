from astar import AStar

from utils import manhattan_distance, Point


class SnakeAStar(AStar[Point]):
    def __init__(self, nodes):
        self.nodes = nodes

    def neighbors(self, n: Point) -> list[Point]:
        return self.nodes[n]

    def distance_between(self, n1: Point, n2: Point) -> float:
        return 1.0

    def heuristic_cost_estimate(self, current: Point, goal: Point) -> float:
        return manhattan_distance(current, goal)

    def is_goal_reached(self, current: Point, goal: Point) -> bool:
        return current == goal
