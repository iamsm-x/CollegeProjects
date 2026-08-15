"""
algorithms.py — Shortest Path Algorithms
=========================================
Implements Dijkstra's Algorithm and A* (A-Star) Algorithm for
campus navigation in Thakur College of Engineering.

Both algorithms use a min-heap (priority queue) for efficiency.

Dijkstra's Algorithm
--------------------
  Classic optimal shortest-path algorithm for weighted graphs.
  Time  : O((V + E) log V)
  Space : O(V)
  Guarantees the globally optimal path.

A* Algorithm
------------
  Heuristic-guided search; explores fewer nodes than Dijkstra.
  Heuristic h(n) = |floor(n) − floor(goal)| × 50
  The heuristic is *admissible* (never overestimates cost)
  because 50 s/floor is the minimum vertical travel time (elevator).
  Time  : O(E log V) in practice
  Space : O(V)
"""

import heapq
import time
try:
    from .graph import NODES, build_adjacency_list, TRANSPORT_STAIRS, TRANSPORT_ELEVATOR
except ImportError:
    from graph import NODES, build_adjacency_list, TRANSPORT_STAIRS, TRANSPORT_ELEVATOR


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _effective_floor(node_id: str) -> int:
    """Return floor number; treat outdoor (floor = -1) as 0 for heuristic."""
    return max(0, NODES[node_id]["floor"])


def _reconstruct_path(prev: dict, destination: str) -> list[str]:
    """Walk backwards through prev-pointers to reconstruct the path."""
    path: list[str] = []
    node = destination
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path


def _generate_directions(path: list[str], prev_transport: dict) -> list[str]:
    """
    Convert a node path into human-readable turn-by-turn directions.

    Consecutive stairs/elevator hops are merged into a single instruction
    (e.g., 'Take stairs up 3 floors to Floor 4').

    Parameters
    ----------
    path           : ordered list of node IDs
    prev_transport : {node_id: transport_type_used_to_reach_it}

    Returns
    -------
    list[str] — one instruction per meaningful navigation step
    """
    if len(path) < 2:
        return [" You are already at your destination!"]

    directions: list[str] = []
    i = 0

    while i < len(path) - 1:
        current   = path[i]
        nxt       = path[i + 1]
        transport = prev_transport.get(nxt, TRANSPORT_STAIRS)

        # ── Stairs block ────────────────────────────────────────────────────
        if transport == TRANSPORT_STAIRS:
            start_floor = _effective_floor(current)
            # Consume the entire consecutive staircase segment
            j = i + 1
            while j < len(path) - 1 and prev_transport.get(path[j + 1]) == TRANSPORT_STAIRS:
                j += 1
            end_floor  = _effective_floor(path[j])
            diff       = abs(end_floor - start_floor)
            direction  = "up ⬆" if end_floor > start_floor else "down ⬇"
            directions.append(
                f" Take the stairs {direction} {diff} floor(s) — "
                f"Floor {start_floor} → Floor {end_floor}  (~{diff * 35}s)"
            )
            i = j  # jump past the whole staircase segment

        # ── Elevator block ───────────────────────────────────────────────────
        elif transport == TRANSPORT_ELEVATOR:
            start_floor = _effective_floor(current)
            j = i + 1
            while j < len(path) - 1 and prev_transport.get(path[j + 1]) == TRANSPORT_ELEVATOR:
                j += 1
            end_floor  = _effective_floor(path[j])
            diff       = abs(end_floor - start_floor)
            direction  = "up ⬆" if end_floor > start_floor else "down ⬇"
            directions.append(
                f" Ride the elevator {direction} {diff} floor(s) — "
                f"Floor {start_floor} → Floor {end_floor}  (~{diff * 30}s, incl. wait)"
            )
            i = j

        # ── Walking step ─────────────────────────────────────────────────────
        else:
            nxt_name = NODES[nxt]["name"]
            nxt_type = NODES[nxt]["type"]

            # Skip intermediate stairs / elevator landings — they appear in
            # the stairs/elevator instructions above.
            if nxt_type in ("stairs", "elevator"):
                i += 1
                continue

            directions.append(f" Walk to  {nxt_name}")
            i += 1

    return directions if directions else ["Walk directly to the destination."]


# ---------------------------------------------------------------------------
# Dijkstra's Algorithm
# ---------------------------------------------------------------------------
def dijkstra(source: str, destination: str, mode: str = "both") -> dict:
    """
    Find the shortest (minimum-time) path using Dijkstra's algorithm.

    Parameters
    ----------
    source      : starting node ID
    destination : target node ID
    mode        : "both" | "stairs" | "elevator"

    Returns
    -------
    dict with keys:
        found              — bool
        path               — list[str]  (node IDs)
        path_names         — list[str]  (human-readable names)
        total_time_seconds — float
        nodes_explored     — int
        compute_time_us    — float  (microseconds)
        directions         — list[str]
        error              — str | None
    """
    t0    = time.perf_counter()
    graph = build_adjacency_list(mode)

    # dist[v] = shortest known time from source to v
    dist: dict[str, float] = {n: float("inf") for n in NODES}
    dist[source] = 0.0

    # For path reconstruction
    prev:           dict[str, str | None] = {n: None for n in NODES}
    prev_transport: dict[str, str | None] = {n: None for n in NODES}

    visited:        set[str] = set()
    nodes_explored: int      = 0

    # Min-heap: (cost, node_id)
    heap = [(0.0, source)]

    while heap:
        cost, u = heapq.heappop(heap)

        if u in visited:          # stale heap entry
            continue
        visited.add(u)
        nodes_explored += 1

        if u == destination:      # early exit
            break

        for v, w, t in graph[u]:
            if v in visited:
                continue
            new_cost = cost + w
            if new_cost < dist[v]:
                dist[v]          = new_cost
                prev[v]          = u
                prev_transport[v] = t
                heapq.heappush(heap, (new_cost, v))

    elapsed_us = (time.perf_counter() - t0) * 1_000_000

    # ── No path found ────────────────────────────────────────────────────────
    if dist[destination] == float("inf"):
        return {
            "found": False, "path": [], "path_names": [],
            "total_time_seconds": -1, "nodes_explored": nodes_explored,
            "compute_time_us": round(elapsed_us, 2), "directions": [],
            "error": (
                f"No path found from '{NODES[source]['name']}' "
                f"to '{NODES[destination]['name']}' with transport mode '{mode}'."
            ),
        }

    path       = _reconstruct_path(prev, destination)
    directions = _generate_directions(path, prev_transport)

    return {
        "found":               True,
        "path":                path,
        "path_names":          [NODES[n]["name"] for n in path],
        "total_time_seconds":  dist[destination],
        "nodes_explored":      nodes_explored,
        "compute_time_us":     round(elapsed_us, 2),
        "directions":          directions,
        "error":               None,
    }


# ---------------------------------------------------------------------------
# A* Heuristic
# ---------------------------------------------------------------------------
def _heuristic(node: str, goal: str) -> float:
    """
    Admissible heuristic for A*.

    h(n) = |floor(n) − floor(goal)| × 30

    Reasoning: the minimum possible time to change one floor is 30 s
    (elevator, floor-to-floor, including wait).  Therefore h never
    overestimates the true cost — making A* optimal.
    """
    return abs(_effective_floor(node) - _effective_floor(goal)) * 30.0


# ---------------------------------------------------------------------------
# A* Algorithm
# ---------------------------------------------------------------------------
def astar(source: str, destination: str, mode: str = "both") -> dict:
    """
    Find the shortest path using the A* (A-Star) algorithm.

    f(n) = g(n) + h(n)
      g(n) : actual travel time from source to n
      h(n) : admissible heuristic — floor-difference × 30 s

    Parameters
    ----------
    source      : starting node ID
    destination : target node ID
    mode        : "both" | "stairs" | "elevator"

    Returns
    -------
    Same dict structure as dijkstra().
    """
    t0    = time.perf_counter()
    graph = build_adjacency_list(mode)

    # g_score[v] = best known actual cost from source to v
    g: dict[str, float] = {n: float("inf") for n in NODES}
    g[source] = 0.0

    prev:           dict[str, str | None] = {n: None for n in NODES}
    prev_transport: dict[str, str | None] = {n: None for n in NODES}

    visited:        set[str] = set()
    nodes_explored: int      = 0

    # Min-heap: (f_score, node_id)
    heap = [(_heuristic(source, destination), source)]

    while heap:
        f, u = heapq.heappop(heap)

        if u in visited:
            continue
        visited.add(u)
        nodes_explored += 1

        if u == destination:
            break

        for v, w, t in graph[u]:
            if v in visited:
                continue
            tentative_g = g[u] + w
            if tentative_g < g[v]:
                g[v]             = tentative_g
                prev[v]          = u
                prev_transport[v] = t
                f_score          = tentative_g + _heuristic(v, destination)
                heapq.heappush(heap, (f_score, v))

    elapsed_us = (time.perf_counter() - t0) * 1_000_000

    # ── No path found ────────────────────────────────────────────────────────
    if g[destination] == float("inf"):
        return {
            "found": False, "path": [], "path_names": [],
            "total_time_seconds": -1, "nodes_explored": nodes_explored,
            "compute_time_us": round(elapsed_us, 2), "directions": [],
            "error": (
                f"No path found from '{NODES[source]['name']}' "
                f"to '{NODES[destination]['name']}' with transport mode '{mode}'."
            ),
        }

    path       = _reconstruct_path(prev, destination)
    directions = _generate_directions(path, prev_transport)

    return {
        "found":               True,
        "path":                path,
        "path_names":          [NODES[n]["name"] for n in path],
        "total_time_seconds":  g[destination],
        "nodes_explored":      nodes_explored,
        "compute_time_us":     round(elapsed_us, 2),
        "directions":          directions,
        "error":               None,
    }


# ---------------------------------------------------------------------------
# Direct script test execution  (python backend/algorithms.py)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    src = "main_gate"
    dst = "library"

    print(f"=== TESTING NAVIGATION: {NODES[src]['name']} -> {NODES[dst]['name']} ===")
    
    dijk = dijkstra(src, dst, mode="elevator")
    print(f"\n[Dijkstra's Algorithm]")
    print(f"  Path Time      : {dijk['total_time_seconds']}s")
    print(f"  Nodes Explored : {dijk['nodes_explored']}")
    print(f"  Compute Time   : {dijk['compute_time_us']} µs")
    print(f"  Path           : {' -> '.join(dijk['path_names'])}")

    ast = astar(src, dst, mode="elevator")
    print(f"\n[A* Algorithm]")
    print(f"  Path Time      : {ast['total_time_seconds']}s")
    print(f"  Nodes Explored : {ast['nodes_explored']}")
    print(f"  Compute Time   : {ast['compute_time_us']} µs")
    print(f"  Path           : {' -> '.join(ast['path_names'])}")
