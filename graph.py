from utils import Point

offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def get_occupied(game_state: dict) -> list[Point]:
    result = []

    for snake in game_state["board"]["snakes"]:
        for cell in snake["body"]:
            result += [Point(cell["x"], cell["y"])]

    return result


def get_food(game_state: dict) -> list[Point]:
    return [Point(cell["x"], cell["y"]) for cell in game_state["board"]["food"]]
    
    
def get_neighbours(cell: Point, game_state: dict) -> list[Point]:
    grid_size_y = game_state["board"]["width"]
    grid_size_x = game_state["board"]["height"]
    occupied_cells = get_occupied(game_state)
    neighbours = [Point(cell.x + o_i, cell.y + o_j) for (o_i, o_j) in offsets]
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
