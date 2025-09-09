game_state_example = """{
  "game": {
    "id": "totally-unique-game-id",
    "ruleset": {
      "name": "standard",
      "version": "v1.1.15",
      "settings": {
        "foodSpawnChance": 15,
        "minimumFood": 1,
        "hazardDamagePerTurn": 14
      }
    },
    "map": "standard",
    "source": "league",
    "timeout": 500
  },
  "turn": 14,
  "board": {
    "height": 11,
    "width": 11,
    "food": [
      {"x": 5, "y": 5},
      {"x": 9, "y": 0},
      {"x": 2, "y": 6}
    ],
    "hazards": [
      {"x": 3, "y": 2}
    ],
    "snakes": [
      {
        "id": "snake-508e96ac-94ad-11ea-bb37",
        "name": "My Snake",
        "health": 54,
        "body": [
          {"x": 0, "y": 0},
          {"x": 1, "y": 0},
          {"x": 2, "y": 0}
        ],
        "latency": "111",
        "head": {"x": 0, "y": 0},
        "length": 3,
        "shout": "why are we shouting??",
        "customizations":{
          "color":"#FF0000",
          "head":"pixel",
          "tail":"pixel"
        }
      },
      {
        "id": "snake-b67f4906-94ae-11ea-bb37",
        "name": "Another Snake",
        "health": 16,
        "body": [
          {"x": 5, "y": 4},
          {"x": 5, "y": 3},
          {"x": 6, "y": 3},
          {"x": 6, "y": 2}
        ],
        "latency": "222",
        "head": {"x": 5, "y": 4},
        "length": 4,
        "shout": "I'm not really sure...",
        "customizations":{
          "color":"#26CF04",
          "head":"silly",
          "tail":"curled"
        }
      }
    ]
  },
  "you": {
    "id": "snake-508e96ac-94ad-11ea-bb37",
    "name": "My Snake",
    "health": 54,
    "body": [
      {"x": 0, "y": 0},
      {"x": 1, "y": 0},
      {"x": 2, "y": 0}
    ],
    "latency": "111",
    "head": {"x": 0, "y": 0},
    "length": 3,
    "shout": "why are we shouting??",
    "customizations": {
      "color":"#FF0000",
      "head":"pixel",
      "tail":"pixel"
    }
  }
}"""

import json

def get_occupied(game_state):
    result = []
    for snake in game_state["board"]["snakes"]:
        for cell in snake["body"]:
            result += [(cell["x"], cell["y"])]
    return result

def get_food(game_state):
    return [(cell["x"], cell["x"]) for cell in game_state["board"]["food"]]
    
    
def get_neighbours(id : (int, int), game_state):
    grid_size_y = game_state["board"]["width"]
    grid_size_x = game_state["board"]["height"]
    occupied_cells = get_occupied(game_state)
    (column_in, row_in) = id
    offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    neighbours = [(column_in+o_i, row_in+o_j) for (o_i, o_j) in offsets]
    neighbours = [(i, j) for (i, j) in neighbours if i>=0 and i < grid_size_x and j>=0 and j<grid_size_y]
    neighbours = [e for e in neighbours if e not in occupied_cells]
    return neighbours

def get_graph(game_state):
    grid_size_x = game_state["board"]["width"]
    grid_size_y = game_state["board"]["height"]
    result = {}
    for i in range(grid_size_x):
        for j in range(grid_size_y):
            result[(i, j)] = get_neighbours((i,j), game_state)
    return result


if __name__ == "__main__":
    game_state = json.loads(game_state_example)
    print(get_neighbours((4, 6), game_state))
    print(get_occupied(game_state))
    #print(get_food(game_state))
    #print(get_graph(game_state))
