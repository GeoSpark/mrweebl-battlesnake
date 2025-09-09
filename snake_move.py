import json
import typing

from neighbours import game_state_example, get_graph
from snake_astar import SnakeAStar


def move(game_state: typing.Dict, graph: list) -> typing.Dict:
    # Aim for the first food in the list.
    goal = game_state['board']['food']

    # Or aim somewhere else. Head for the centre of the board :shrug:
    if len(goal) == 0:
        goal = (5, 5)
    else:
        goal = (goal[0]['x'], goal[0]['y'])

    head = (game_state["you"]["head"]["x"], game_state["you"]["head"]["y"])

    path = SnakeAStar(graph).astar(head, goal)

    if path is None:
        return {"move": "up"}

    # The first node is the head, so we skip it.
    foo = list(path)
    node = foo[1]

    if node[0] < head[0]:
        return {"move": "left"}
    elif node[0] > head[0]:
        return {"move": "right"}
    elif node[1] < head[1]:
        return {"move": "down"}
    elif node[1] > head[1]:
        return {"move": "up"}

    return {"move": "up"}



if __name__ == "__main__":
    game_state = json.loads(game_state_example)

    graph = get_graph(game_state)
    m = move(game_state, graph)
    print(m)
