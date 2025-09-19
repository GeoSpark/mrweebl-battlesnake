# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com
from dataclasses import asdict

from graph import get_graph
from move import move_astar


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "JD",
        "color": "#8600b3",
        "head": "all-seeing",
        "tail": "freckled",
    }


# start is called when your Battlesnake begins a game
def start(game_state: dict) -> None:
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: dict) -> None:
    print("GAME OVER\n")


def move(game_state: dict) -> dict:
    graph = get_graph(game_state)
    m = move_astar(game_state, graph)

    return asdict(m)


if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
