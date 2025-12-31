"""
Shared data models for game entities that may exist on both
client and server (players, missiles, etc.).
"""

from dataclasses import dataclass


@dataclass
class Missile:
    """
    Simple straight-line projectile (e.g., Ezreal Q style).

    - (x, y): current world position
    - (vx, vy): normalized direction vector (unit length)
    - speed: world units per second
    - max_distance: how far it can travel before despawning
    - traveled: distance traveled so far
    - active: whether the missile is still alive (for cleanup)
    - direction: 'up' | 'down' | 'left' | 'right' for sprite facing
    """
    x: float
    y: float
    vx: float
    vy: float
    speed: float
    max_distance: float
    traveled: float = 0.0
    active: bool = True
    direction: str = "right"


@dataclass
class Boss:
    """
    Simple chasing enemy boss that walks toward the player and deals
    damage when close.

    - (row, col): current grid position
    - (x, y): current world position (isometric)
    - health / max_health: boss vitality
    - speed: world units per second
    """

    row: int
    col: int
    x: float
    y: float
    speed: float
    health: float
    max_health: float
