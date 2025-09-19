offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def get_occupied(game_state: dict):
    result = []

    for snake in game_state["board"]["snakes"]:
        for cell in snake["body"]:
            result += [(cell["x"], cell["y"])]

    return result


def get_food(game_state):
    return [(cell["x"], cell["y"]) for cell in game_state["board"]["food"]]
    
    
def get_neighbours(cell : tuple[int, int], game_state: dict):
    grid_size_y = game_state["board"]["width"]
    grid_size_x = game_state["board"]["height"]
    occupied_cells = get_occupied(game_state)
    (column_in, row_in) = cell
    neighbours = [(column_in+o_i, row_in+o_j) for (o_i, o_j) in offsets]
    neighbours = [(i, j) for (i, j) in neighbours if 0 <= i < grid_size_x and 0 <= j < grid_size_y]
    neighbours = [e for e in neighbours if e not in occupied_cells]
    return neighbours


def get_graph(game_state: dict):
    grid_size_x = game_state["board"]["width"]
    grid_size_y = game_state["board"]["height"]
    result = {}
    for i in range(grid_size_x):
        for j in range(grid_size_y):
            result[(i, j)] = get_neighbours((i, j), game_state)

    return result
