import typing

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

    node = list(path)[0]

    if node[0] < head[0]:
        return {"move": "left"}
    elif node[0] > head[0]:
        return {"move": "right"}
    elif node[1] < head[1]:
        return {"move": "down"}
    elif node[1] > head[1]:
        return {"move": "up"}

    return {"move": "up"}
