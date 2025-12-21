"""
Dijkstra pathfinding on a 2D grid with full 8-direction movement
and diagonal corner-blocking rules.

Grid is expected to be a 2D list of:
    0 = walkable
    1 = obstacle (water)
"""

import heapq
import math
from typing import List, Tuple, Optional


Grid = List[List[int]]
Cell = Tuple[int, int]


def dijkstra(grid: Grid, start: Cell, goal: Cell) -> List[Cell]:
    """
    Compute a path from start → goal using Dijkstra's algorithm.
    Returns:
        list of (row, col) cells if reachable
        [] if no path exists
    """
    num_rows = len(grid)
    num_cols = len(grid[0])

    distance = [[float("inf")] * num_cols for _ in range(num_rows)]
    distance[start[0]][start[1]] = 0.0

    previous: List[List[Optional[Cell]]] = [
        [None] * num_cols for _ in range(num_rows)
    ]

    pq = [(0.0, start)]

    # 8-direction movement
    directions = [
        (-1,  0), (1,  0), (0, -1), (0, 1),    # orthogonal
        (-1, -1), (-1, 1), (1, -1), (1, 1)     # diagonals
    ]

    while pq:
        current_dist, (row, col) = heapq.heappop(pq)

        if current_dist > distance[row][col]:
            continue

        if (row, col) == goal:
            break

        for dr, dc in directions:
            nr, nc = row + dr, col + dc

            # Bounds check
            if not (0 <= nr < num_rows and 0 <= nc < num_cols):
                continue

            # Obstacle check
            if grid[nr][nc] == 1:
                continue

            # Diagonal corner-cutting prevention
            if dr != 0 and dc != 0:
                adj1 = (row + dr, col)
                adj2 = (row, col + dc)
                if grid[adj1[0]][adj1[1]] == 1 or grid[adj2[0]][adj2[1]] == 1:
                    continue

            # Cost: straight = 1, diagonal = sqrt(2)
            move_cost = 1.0 if dr == 0 or dc == 0 else math.sqrt(2)
            new_dist = current_dist + move_cost

            if new_dist < distance[nr][nc]:
                distance[nr][nc] = new_dist
                previous[nr][nc] = (row, col)
                heapq.heappush(pq, (new_dist, (nr, nc)))

    # If unreached → no path
    if distance[goal[0]][goal[1]] == float("inf"):
        return []

    # Reconstruct path
    path = []
    cell: Optional[Cell] = goal
    while cell:
        path.append(cell)
        r, c = cell
        cell = previous[r][c]

    path.reverse()
    return path
