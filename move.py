from graph import get_neighbours, get_food
from snake_astar import SnakeAStar
from utils import manhattan_distance, Point, MoveResponse


def move_astar(game_state: dict, graph: dict[Point, list[Point]]) -> MoveResponse:
    foods = get_food(game_state)
    head = Point(game_state["you"]["head"]["x"], game_state["you"]["head"]["y"])
    neighbours = get_neighbours(head, game_state)

    if len(neighbours) == 0:
        neighbours = get_neighbours(head, game_state, ignore_halo=True)

        if len(neighbours) == 0:
            return MoveResponse(move="up", shout="Oh bugger.")

    # TODO: If an enemy snake is closer to the food, choose another.
    # TODO: If the food has zero or one neighbour, choose another.
    # TODO: If there's no other way out, find the largest subgraph and pick a point there.
    # Seek the nearest food first, otherwise the first neighbour.
    goals = sorted(foods, key=lambda food: manhattan_distance(food, head))
    # print(f"Head: {head} Goals: {goals}")
    # TODO: Pick a better last-resort goal.
    path = [neighbours[0]]
    a_star = SnakeAStar(graph)

    for g in goals:
        p = a_star.astar(head, g)

        if p is not None:
            # The first node is the head, so we skip it.
            path = list(p)[1:]
            # The path doesn't include the goal.
            path.append(g)
            break

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
