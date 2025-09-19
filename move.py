from graph import get_neighbours, get_food
from snake_astar import SnakeAStar
from utils import manhattan_distance, Point, MoveResponse


def move_astar(game_state: dict, graph: dict[Point, list[Point]]) -> MoveResponse:
    foods = get_food(game_state)
    head = Point(game_state["you"]["head"]["x"], game_state["you"]["head"]["y"])
    neighbours = get_neighbours(head, game_state)

    if len(neighbours) == 0:
        return MoveResponse(move="up", shout="Oh bugger.")

    # Seek the nearest food first, otherwise the first neighbour.
    goals = sorted(foods, key=lambda food: manhattan_distance(food, head))
    goals.append(neighbours[0])
    # print(f"Head: {head} Goals: {goals}")
    path = None
    goal = None

    for g in goals:
        path = SnakeAStar(graph).astar(head, g)

        if path is not None:
            goal = g
            break

    if goal is None or path is None:
        # We shouldn't get here because we'll always have at least a neighbour.
        raise NotImplementedError()

    # The first node is the head, so we skip it.
    path = list(path)[1:]
    path.append(goal)

    move = build_move(head, path[0])

    return MoveResponse(move=move, shout="Badger, badger, badger, mushroom!")


def build_move(head: Point, node: Point):
    if node.x < head.x:
        move = "left"
    elif node.x > head.x:
        move = "right"
    elif node.y < head.y:
        move = "down"
    else:
        move = "up"

    return move
