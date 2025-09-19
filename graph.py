from utils import Point

offsets = [Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)]


def get_occupied(game_state: dict, ignore_halo) -> set[Point]:
    result = set()
    my_id = game_state["you"]["id"]

    # Avoid all bodies.
    for snake in game_state["board"]["snakes"]:
        for cell in snake["body"]:
            result.add(Point(cell["x"], cell["y"]))

        # Avoid the halo around other snakes' heads.
        if not ignore_halo and snake["id"] != my_id:
            result.add(Point(snake["head"]["x"], snake["head"]["y"]) + offsets[0])
            result.add(Point(snake["head"]["x"], snake["head"]["y"]) + offsets[1])
            result.add(Point(snake["head"]["x"], snake["head"]["y"]) + offsets[2])
            result.add(Point(snake["head"]["x"], snake["head"]["y"]) + offsets[3])

    return result


def get_food(game_state: dict) -> list[Point]:
    return [Point(cell["x"], cell["y"]) for cell in game_state["board"]["food"]]
    
    
def get_neighbours(cell: Point, game_state: dict, ignore_halo=False) -> list[Point]:
    grid_size_x = game_state["board"]["width"]
    grid_size_y = game_state["board"]["height"]
    occupied_cells = get_occupied(game_state, ignore_halo)
    neighbours = [cell + o for o in offsets]
    neighbours = [p for p in neighbours if 0 <= p.x < grid_size_x and 0 <= p.y < grid_size_y]
    neighbours = [e for e in neighbours if e not in occupied_cells]

    return neighbours


def get_graph(game_state: dict) -> dict[Point, list[Point]]:
    grid_size_x = game_state["board"]["width"]
    grid_size_y = game_state["board"]["height"]
    result = {}

    for i in range(grid_size_x):
        for j in range(grid_size_y):
            result[Point(i, j)] = get_neighbours(Point(i, j), game_state)

    return result
