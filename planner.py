# simple_battlesnake.py
# -----------------------------------------------------------------------------
# Stateless move chooser using only NetworkX and (x, y) tuple nodes.
#
# Rules implemented:
# 1) Move toward the largest open space (directional: past the first step).
# 2) If already at (or tied for) the largest open space, pick a random nearby
#    cell among the best directions.
# 3) If hungry, prefer food that lies inside the largest open space(s).
#    Move along a shortest path toward the nearest such food.
# 4) If the opponent head is "close", avoid stepping into its head square or
#    any square it could move into next turn. If all moves are threatened,
#    fall back to the unfiltered legal moves.
#
# No cross-turn state. Nodes are plain (x, y) tuples.
# -----------------------------------------------------------------------------

from __future__ import annotations
from typing import Iterable, Optional, Tuple, Dict, Set, List
import random
import networkx as nx

from utils import Point

Coord = Point


# ──────────────────────────────────────────────────────────────────────────────
# Small helpers
# ──────────────────────────────────────────────────────────────────────────────

def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbours4(p: Coord, width: int, height: int) -> List[Coord]:
    x, y = p
    out = []
    if x > 0: out.append((x - 1, y))
    if x + 1 < width: out.append((x + 1, y))
    if y > 0: out.append((x, y - 1))
    if y + 1 < height: out.append((x, y + 1))
    return out


# ──────────────────────────────────────────────────────────────────────────────
# Graph construction
# ──────────────────────────────────────────────────────────────────────────────

def build_open_graph(width: int, height: int, blocked: Iterable[Coord], head: Coord) -> nx.Graph:
    """
    Create a 4-neighbour grid and remove blocked nodes, except we keep `head`
    so reachability and paths are computable from the current position.
    """
    G = nx.grid_2d_graph(width, height)  # nodes are (x, y) tuples
    blocked_set = set(blocked)
    blocked_set.discard(head)
    G.remove_nodes_from([b for b in blocked_set if b in G])
    return G


# ──────────────────────────────────────────────────────────────────────────────
# Directional space: size of the area if we step into each neighbour
# ──────────────────────────────────────────────────────────────────────────────

def directional_spaces(H: nx.Graph, head: Coord) -> Tuple[Dict[Coord, int], Dict[Coord, Set[Coord]]]:
    """
    Compute, for each neighbour n of `head`, the size and node set of the
    connected component reachable from n when the head node is removed.
    Returns:
      size_by_n[n]: int
      area_by_n[n]: set of coords in that component
    """
    if head not in H:
        return {}, {}

    H_minus_head = H.copy()
    H_minus_head.remove_node(head)

    # Build a mapping from node -> component set once (cheap on small boards)
    comp_sets: List[Set[Coord]] = [set(c) for c in nx.connected_components(H_minus_head)]
    node_to_comp: Dict[Coord, Set[Coord]] = {}
    for comp in comp_sets:
        for v in comp:
            node_to_comp[v] = comp

    size_by_n: Dict[Coord, int] = {}
    area_by_n: Dict[Coord, Set[Coord]] = {}
    for n in H.neighbors(head):
        comp = node_to_comp.get(n)
        if comp is None:
            continue
        area_by_n[n] = comp
        size_by_n[n] = len(comp)
    return size_by_n, area_by_n


# ──────────────────────────────────────────────────────────────────────────────
# Opponent hazard ring (local, simple)
# ──────────────────────────────────────────────────────────────────────────────

def hazard_cells(width: int, height: int, my_head: Coord, opp_head: Optional[Coord], threat_radius: int) -> Set[Coord]:
    """
    If the opponent head is within `threat_radius` (Manhattan), avoid its cell
    and any cell it could move into next turn.
    """
    if opp_head is None:
        return set()
    if manhattan(my_head, opp_head) > threat_radius:
        return set()
    return {opp_head, *neighbours4(opp_head, width, height)}


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────


def choose_next_step(
    width: int,
    height: int,
    head: Coord,
    blocked: Iterable[Coord],
    foods: Iterable[Coord],
    hungry: bool,
    opponent_head: Optional[Coord] = None,
    threat_radius: int = 3,
    rnd: random.Random = random,
) -> Optional[Coord]:
    """
    Stateless move chooser:
      - Hungry: go to nearest food inside the largest directional space(s).
      - Not hungry: go to centre of the largest space; if already there,
        go to centre of the next-largest space; else pick the neighbour with
        greatest local degree (options), breaking ties away from the opponent.
    """
    H = build_open_graph(width, height, blocked, head)
    if head not in H:
        return None

    legal = [n for n in H.neighbors(head)]
    if not legal:
        return None

    # Avoid opponent's immediate reach if close
    hazards = hazard_cells(width, height, head, opponent_head, threat_radius)
    safe_legal = [n for n in legal if n not in hazards] or legal  # fall back if all hazardous

    # Directional spaces (with head removed)
    size_by_n, area_by_n = directional_spaces(H, head)
    if not size_by_n:  # degenerate: just move safely
        return rnd.choice(safe_legal)

    # Build unique areas ranked by size (largest first)
    # Several neighbours can lead into the same area; we collapse them.
    areas = {}
    for n, area in area_by_n.items():
        key = frozenset(area)
        rec = areas.setdefault(key, {"size": len(area), "area": area, "neighs": []})
        rec["neighs"].append(n)
    ranked = sorted(areas.values(), key=lambda r: r["size"], reverse=True)
    best = ranked[0]
    foods_set = set(foods)

    # Helper: step toward a target node, preferring a safe first step
    def step_toward(target: Coord) -> Optional[Coord]:
        if target not in H or head not in H:
            return None
        try:
            path = nx.shortest_path(H, head, target)
            if len(path) >= 2 and path[1] in safe_legal:
                return path[1]
        except nx.NetworkXNoPath:
            pass
        # If the exact next step is hazardous, choose the safe neighbour that gets closest to target
        try:
            dist_to_target = nx.single_source_shortest_path_length(H, target)
            candidates = [n for n in safe_legal if n in dist_to_target]
            if candidates:
                return min(candidates, key=lambda n: dist_to_target[n])
        except nx.NetworkXError:
            pass
        return None

    # Compute centre(s) of an area; pick the one closest to our head
    def area_centre(area: Set[Coord]) -> Optional[Coord]:
        if not area:
            return None
        H_area = H.subgraph(area)
        try:
            centres = list(nx.center(H_area))
        except nx.NetworkXError:
            centres = []
        if not centres:
            return None
        d_from_head = nx.single_source_shortest_path_length(H, head)
        return min(centres, key=lambda c: d_from_head.get(c, 10**9))

    # ── Hungry: prefer food inside the largest area(s)
    if hungry and foods_set:
        # Among neighbours that lead into an area containing food and having max size,
        # pick the nearest such food.
        max_size = best["size"]
        best_dirs = [
            n for n, sz in size_by_n.items()
            if sz == max_size and (area_by_n.get(n, set()) & foods_set)
        ]
        if best_dirs:
            d_from_head = nx.single_source_shortest_path_length(H, head)
            best_food, best_dir, best_dist = None, None, 10**9
            for n in best_dirs:
                for f in area_by_n[n] & foods_set:
                    d = d_from_head.get(f)
                    if d is not None and d < best_dist:
                        best_food, best_dir, best_dist = f, n, d
            if best_food is not None:
                step = step_toward(best_food)
                if step is not None:
                    return step
                if best_dir in safe_legal:
                    return best_dir
        # If no food lies in the largest area(s), we fall through to the non-hungry logic.

    # ── Not hungry (or hungry but no food in largest area): go to centre of largest area
    centre1 = area_centre(best["area"])
    if centre1 is not None and head != centre1:
        step = step_toward(centre1)
        if step is not None:
            return step

    # Already at the centre of the largest area (or centre is undefined):
    # Strategy: head to the centre of the next-largest area (if any).
    if len(ranked) > 1:
        second = ranked[1]
        centre2 = area_centre(second["area"])
        if centre2 is not None:
            step = step_toward(centre2)
            if step is not None:
                return step
        # If stepping along the exact path is blocked by hazards, we’ll drop to the local rule below.

    # No second area (or couldn’t step safely): pick neighbour with highest local degree
    # in H with head removed (keeps options); tie-break by distance from opponent head.
    H_minus_head = H.copy()
    H_minus_head.remove_node(head)
    def local_degree(n: Coord) -> int:
        return H_minus_head.degree(n) if n in H_minus_head else 0
    def away_from_opp(n: Coord) -> int:
        return manhattan(n, opponent_head) if opponent_head is not None else 0

    candidates = [n for n in safe_legal]
    if not candidates:
        candidates = legal  # absolute fallback

    # Maximise (degree, distance from opponent)
    best_n = max(candidates, key=lambda n: (local_degree(n), away_from_opp(n)))
    return best_n
