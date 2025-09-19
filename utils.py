def distance(p1, p2) -> float:
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def manhattan_distance(p1, p2) -> float:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
