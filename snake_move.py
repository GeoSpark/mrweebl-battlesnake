from neighbours import get_neighbours, get_food
from snake_astar import SnakeAStar
from utils import manhattan_distance


def move_astar(game_state: dict, graph: list) -> dict:
    foods = get_food(game_state)
    head = (game_state["you"]["head"]["x"], game_state["you"]["head"]["y"])
    neighbours = get_neighbours(head, game_state)

    if len(neighbours) == 0:
        return {"move": "up", "shout": "Oh bugger."}

    goals = sorted(foods, key=lambda x: manhattan_distance(x, head))
    goals.append(neighbours[0])
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

    return {"move": move, "shout": "Badger, badger, badger, mushroom!"}


def build_move(head: tuple[int, int], node: tuple[int, int]):
    if node[0] < head[0]:
        move = "left"
    elif node[0] > head[0]:
        move = "right"
    elif node[1] < head[1]:
        move = "down"
    else:
        move = "up"

    return move
