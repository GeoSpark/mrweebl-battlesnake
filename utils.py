from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"<{self.x} {self.y}>"


@dataclass()
class MoveResponse:
    move: str
    shout: str = ""

def distance(p1: Point, p2: Point) -> float:
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


def manhattan_distance(p1, p2) -> float:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)
