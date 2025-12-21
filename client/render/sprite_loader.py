"""
Sprite loading utilities for the client.

We load:
- Player sprites: up, down, left, right
- Missile sprites: up, down, left, right
"""

import os
import pygame


class PlayerSprites:
    """
    Container for the 4 directional sprites for the player.
    """

    def __init__(self, up: pygame.Surface, down: pygame.Surface,
                 left: pygame.Surface, right: pygame.Surface):
        self.up = up
        self.down = down
        self.left = left
        self.right = right


class MissileSprites:
    """
    Container for the 4 directional sprites for missiles.
    """

    def __init__(self, up: pygame.Surface, down: pygame.Surface,
                 left: pygame.Surface, right: pygame.Surface):
        self.up = up
        self.down = down
        self.left = left
        self.right = right


def _load_and_scale(base_path: str, filename: str, scale: float) -> pygame.Surface:
    full_path = os.path.join(base_path, filename)
    image = pygame.image.load(full_path).convert_alpha()

    if scale != 1.0:
        w, h = image.get_size()
        new_size = (int(w * scale), int(h * scale))
        image = pygame.transform.smoothscale(image, new_size)

    return image


def load_player_sprites(
    base_path: str = "assets/sprites/player",
    scale: float = 0.5,  # tweak this as you like
) -> PlayerSprites:
    """
    Load the 4 basic directional sprites for the player.
    Expected filenames:
        up.png, down.png, left.png, right.png
    """
    up = _load_and_scale(base_path, "up.png", scale)
    down = _load_and_scale(base_path, "down.png", scale)
    left = _load_and_scale(base_path, "left.png", scale)
    right = _load_and_scale(base_path, "right.png", scale)

    return PlayerSprites(up=up, down=down, left=left, right=right)


def load_missile_sprites(
    base_path: str = "assets/sprites/missiles",
    scale: float = 0.3,  # can be different from player scale if you want
) -> MissileSprites:
    """
    Load the 4 basic directional sprites for missiles.
    Expected filenames:
        up.png, down.png, left.png, right.png
    """
    up = _load_and_scale(base_path, "up.png", scale)
    down = _load_and_scale(base_path, "down.png", scale)
    left = _load_and_scale(base_path, "left.png", scale)
    right = _load_and_scale(base_path, "right.png", scale)

    return MissileSprites(up=up, down=down, left=left, right=right)
