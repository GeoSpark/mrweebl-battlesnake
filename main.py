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
import random
from dataclasses import asdict

from move import choose_move


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> dict:
    return {
        "apiversion": "1",
        "author": "JD",
        "color": f"#{random.randint(0, 0xFFFFFF):06x}",  # "#8600b3",
        "head": "all-seeing",
        "tail": "freckled",
        "version": "2.0"
    }


# start is called when your Battlesnake begins a game
def start(game_state: dict) -> None:
    name = game_state["you"]["name"]
    print(f"Game start {name}")


# end is called when your Battlesnake finishes a game
def end(game_state: dict) -> None:
    name = game_state["you"]["name"]
    print(f"Game over {name}")


def move(game_state: dict) -> dict:
    m = choose_move(game_state)

    return asdict(m)


if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
