from graph import get_food, get_heads, get_occupied, get_lengths
from planner import choose_next_step
from utils import Point, MoveResponse


def _build_move(head: Point, node: Point):
    if node.x < head.x:
        move = "left"
    elif node.x > head.x:
        move = "right"
    elif node.y < head.y:
        move = "down"
    else:
        move = "up"

    return move

def choose_move(game_state: dict):
    board_width = game_state["board"]["width"]
    board_height = game_state["board"]["height"]
    blocked_cells = get_occupied(game_state, ignore_halo=True)
    my_head = Point(game_state["you"]["head"]["x"], game_state["you"]["head"]["y"])
    food_cells = get_food(game_state)
    my_health = game_state["you"]["health"]
    heads = get_heads(game_state)
    their_length = get_lengths(game_state)[0]
    my_length = game_state["you"]["length"]
    turn = game_state["turn"]

    # Because we have some agressive opponents, allow for potential head-to-heads by
    # ensuring we're at least as long as the opponent. If we are longer and there is a
    # cell we're both likely to go for, choose it so we win any head-to-heads.
    should_eat = (my_length <= their_length) or (my_health < 30)
    # This is a bit of a risk because head-to-heads of equal-length snakes causes
    # both to be eliminated.
    threat_radius = 2 if (my_length < their_length) else 0

    # print(f"{turn} - ", end="")

    dest = choose_next_step(
        board_width,
        board_height,
        my_head,
        blocked_cells,
        food_cells,
        should_eat,
        opponent_head=None if len(heads) == 0 else heads[0],
        opponent_length=their_length,
        threat_radius=threat_radius,
    )

    if dest is not None:
        move = _build_move(my_head, Point(dest[0], dest[1]))
    else:
        move = "up"

    return MoveResponse(move=move, shout="Badger, badger, badger, mushroom!")
