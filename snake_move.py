import json
import typing

from neighbours import game_state_example, get_graph, get_neighbours
from snake_astar import SnakeAStar


def move_astar(game_state: typing.Dict, graph: list) -> typing.Dict:
    # Aim for the first food in the list.
    foods = game_state['board']['food']
    head = (game_state["you"]["head"]["x"], game_state["you"]["head"]["y"])

    # Or aim somewhere else. Head for the centre of the board :shrug:
    goal = (5, 5)
    dist = 99999

    for food in foods:
        f1 = (food['x'], food['y'])
        d1 = abs(f1[0] - head[0]) + abs(f1[1] - head[1])

        if d1 < dist:
            dist = d1
            goal = f1

    get_neighbours(head, game_state)

    path = SnakeAStar(graph).astar(head, goal)

    if path is None:
        return {"move": "up"}

    # The first node is the head, so we skip it.
    foo = list(path)
    # We are next to the food, so just move there.
    if len(foo) == 1:
        node = goal
    else:
        node = foo[1]

    if node[0] < head[0]:
        return {"move": "left"}
    elif node[0] > head[0]:
        return {"move": "right"}
    elif node[1] < head[1]:
        return {"move": "down"}
    elif node[1] > head[1]:
        return {"move": "up"}

    return {"move": "up", "shout": "Badger, badger, badger, mushroom!"}



if __name__ == "__main__":
    game_state = json.loads(game_state_example)

    graph = get_graph(game_state)
    m = move_astar(game_state, graph)
    print(m)
