"""
Helper functions for converting between grid coordinates,
world isometric coordinates, and screen coordinates.
"""

from shared.constants import TILE_WIDTH, TILE_HEIGHT


def grid_to_world(row: int, col: int):
    """
    Convert (row, col) grid coordinates into world-space isometric coordinates.
    Returns (x_world, y_world).
    """
    x_world = (col - row) * (TILE_WIDTH // 2)
    y_world = (col + row) * (TILE_HEIGHT // 2)
    return x_world, y_world


def world_to_screen(x_world: float, y_world: float, camera_x: float, camera_y: float):
    """
    Convert world coordinates into screen coordinates using camera offsets.
    """
    return x_world + camera_x, y_world + camera_y


def screen_to_world(x_screen: float, y_screen: float, camera_x: float, camera_y: float):
    """
    Convert screen coordinates (pixel space) into world coordinates
    by removing the camera offset.
    """
    return x_screen - camera_x, y_screen - camera_y


def screen_to_grid(x_screen: float, y_screen: float, camera_x: float, camera_y: float):
    """
    Convert screen coordinates (mouse position or tile position on display)
    into grid coordinates (row, col).
    This performs:
      1. Remove camera offset → world coords
      2. Reverse the isometric transform
      3. Round to nearest tile
    """
    # Step 1: remove camera offset to get world coordinates
    x_world = x_screen - camera_x
    y_world = y_screen - camera_y

    half_w = TILE_WIDTH / 2.0
    half_h = TILE_HEIGHT / 2.0

    # Invert the isometric transform
    col = (x_world / half_w + y_world / half_h) / 2.0
    row = (y_world / half_h - x_world / half_w) / 2.0

    return int(round(row)), int(round(col))


def grid_world_bounds(rows: int, cols: int):
    """
    Compute an axis-aligned bounding box for an isometric grid.

    This returns (min_x, max_x, min_y, max_y) in world coordinates and
    expands the extents by half a tile so the outermost tiles stay visible
    when the camera is clamped.
    """
    corners = (
        grid_to_world(0, 0),
        grid_to_world(rows - 1, 0),
        grid_to_world(0, cols - 1),
        grid_to_world(rows - 1, cols - 1),
    )

    xs = [x for x, _ in corners]
    ys = [y for _, y in corners]

    half_w = TILE_WIDTH // 2
    half_h = TILE_HEIGHT // 2

    min_x = min(xs) - half_w
    max_x = max(xs) + half_w
    min_y = min(ys) - half_h
    max_y = max(ys) + half_h

    return min_x, max_x, min_y, max_y
