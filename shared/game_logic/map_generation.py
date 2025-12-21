"""
Procedural generation for the grid:
- Create base grid
- Add water patches
"""

import random
from typing import List, Tuple

Grid = List[List[int]]


def create_grid(rows: int, cols: int, seed: int = None) -> Grid:
    """
    Create a fresh grid initialized with walkable land.
    """
    if seed is not None:
        random.seed(seed)

    return [[0 for _ in range(cols)] for _ in range(rows)]


def generate_water_patches(
    grid: Grid,
    num_patches: int = 120,
    min_size: int = 5,
    max_size: int = 20
):
    """
    Procedurally carve out water tiles in patch-like clusters.
    Water = 1
    Land = 0
    """
    rows = len(grid)
    cols = len(grid[0])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for _ in range(num_patches):

        # Try up to 50 random start attempts
        for _try in range(50):
            r = random.randint(0, rows - 1)
            c = random.randint(0, cols - 1)
            if grid[r][c] == 0 and not (r == 0 and c == 0):
                break
        else:
            # Could not find a starting point
            continue

        patch_size = random.randint(min_size, max_size)
        frontier = [(r, c)]
        grid[r][c] = 1

        patch_tiles = [(r, c)]

        # Grow cluster
        while frontier and len(patch_tiles) < patch_size:
            fr, fc = random.choice(frontier)
            random.shuffle(directions)

            grew = False

            for dr, dc in directions:
                nr = fr + dr
                nc = fc + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    # Don't overwrite land at (0,0)
                    if grid[nr][nc] == 0 and not (nr == 0 and nc == 0):
                        grid[nr][nc] = 1
                        frontier.append((nr, nc))
                        patch_tiles.append((nr, nc))
                        grew = True

                        if len(patch_tiles) >= patch_size:
                            break

            if not grew:
                frontier.remove((fr, fc))
