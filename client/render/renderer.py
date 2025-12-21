"""
Rendering for the isometric grid, path, player, and missiles.
"""

import pygame

from shared.constants import (
    TILE_WIDTH,
    TILE_HEIGHT,
    COLOR_BACKGROUND,
    COLOR_LAND,
    COLOR_WATER,
    COLOR_PATH,
    COLOR_PLAYER,      # still handy if you ever want circle fallback
    COLOR_Q_MISSILE,
    Q_MISSILE_RADIUS,  # unused now but kept in case you want circles again
    HEALTH_BAR_WIDTH,
    HEALTH_BAR_HEIGHT,
    COLOR_HEALTH_BG,
    COLOR_HEALTH_FILL,
    COLOR_HEALTH_BORDER,
    COLOR_BOSS,
    BOSS_ATTACK_RANGE,
)
from shared.game_logic.isometric import grid_to_world, world_to_screen
from client.game.local_state import LocalState
from client.game.camera import Camera
from client.render.sprite_loader import (
    load_player_sprites,
    PlayerSprites,
    load_missile_sprites,
    MissileSprites,
)
from client.render.ui import HealthBarRenderer


class Renderer:
    """
    Responsible for drawing the game world to the screen surface.
    """

    def __init__(self, screen: pygame.Surface, screen_width: int, screen_height: int):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load player directional sprites once
        self.player_sprites: PlayerSprites = load_player_sprites()
        # Load missile directional sprites
        self.missile_sprites: MissileSprites = load_missile_sprites()
        self.health_bar = HealthBarRenderer(
            width=HEALTH_BAR_WIDTH,
            height=HEALTH_BAR_HEIGHT,
            bg_color=COLOR_HEALTH_BG,
            fill_color=COLOR_HEALTH_FILL,
            border_color=COLOR_HEALTH_BORDER,
        )

    def render(self, state: LocalState, camera: Camera) -> None:
        """
        Render the full frame.
        """
        self.screen.fill(COLOR_BACKGROUND)

        self._draw_tiles(state, camera)
        self._draw_path(state, camera)
        self._draw_missiles(state, camera)
        self._draw_boss(state, camera)
        self._draw_player(state, camera)

    # ---------- Internal helpers ----------

    def _draw_tiles(self, state: LocalState, camera: Camera) -> None:
        """
        Draw the isometric tiles with basic culling.
        """
        grid = state.grid
        rows = state.grid_rows
        cols = state.grid_cols

        for row in range(rows):
            for col in range(cols):
                tile_world_x, tile_world_y = grid_to_world(row, col)
                tile_x, tile_y = world_to_screen(
                    tile_world_x,
                    tile_world_y,
                    camera.x,
                    camera.y,
                )

                # Cull tiles far off-screen
                if (tile_x + TILE_WIDTH < 0 or
                    tile_x - TILE_WIDTH > self.screen_width or
                    tile_y + TILE_HEIGHT < 0 or
                    tile_y - TILE_HEIGHT > self.screen_height):
                    continue

                # Diamond corners (isometric tile)
                top = (int(tile_x), int(tile_y - TILE_HEIGHT // 2))
                right = (int(tile_x + TILE_WIDTH // 2), int(tile_y))
                bottom = (int(tile_x), int(tile_y + TILE_HEIGHT // 2))
                left = (int(tile_x - TILE_WIDTH // 2), int(tile_y))

                color = COLOR_LAND if grid[row][col] == 0 else COLOR_WATER
                pygame.draw.polygon(self.screen, color, [top, right, bottom, left])

    def _draw_path(self, state: LocalState, camera: Camera) -> None:
        """
        Draw the player's current path as small yellow dots.
        """
        for (row, col) in state.current_path:
            tile_world_x, tile_world_y = grid_to_world(row, col)
            x, y = world_to_screen(
                tile_world_x,
                tile_world_y,
                camera.x,
                camera.y,
            )

            if -10 < x < self.screen_width + 10 and -10 < y < self.screen_height + 10:
                pygame.draw.circle(
                    self.screen,
                    COLOR_PATH,
                    (int(x), int(y - 6)),
                    2,
                )

    def _get_missile_sprite(self, direction: str) -> pygame.Surface:
        """
        Return the correct sprite surface based on missile direction.
        """
        if direction == "up":
            return self.missile_sprites.up
        elif direction == "down":
            return self.missile_sprites.down
        elif direction == "left":
            return self.missile_sprites.left
        elif direction == "right":
            return self.missile_sprites.right
        # Fallback
        return self.missile_sprites.right

    def _draw_missiles(self, state: LocalState, camera: Camera) -> None:
        """
        Draw active missiles as directional sprites.
        """
        for missile in state.missiles:
            if not missile.active:
                continue

            screen_x, screen_y = world_to_screen(
                missile.x,
                missile.y,
                camera.x,
                camera.y,
            )

            sprite = self._get_missile_sprite(missile.direction)
            rect = sprite.get_rect()

            # Center the missile sprite on its world position, with a small vertical lift
            draw_x = int(screen_x - rect.width / 2)
            draw_y = int(screen_y - rect.height / 2 - 6)

            self.screen.blit(sprite, (draw_x, draw_y))

    def _get_player_sprite(self, facing_direction: str) -> pygame.Surface:
        """
        Return the correct sprite surface based on the player's facing direction.
        """
        if facing_direction == "up":
            return self.player_sprites.up
        elif facing_direction == "down":
            return self.player_sprites.down
        elif facing_direction == "left":
            return self.player_sprites.left
        elif facing_direction == "right":
            return self.player_sprites.right
        # Fallback
        return self.player_sprites.down

    def _draw_player(self, state: LocalState, camera: Camera) -> None:
        """
        Draw the player as a sprite facing the current direction.
        We treat the tile center as the player's "feet" and align
        the sprite so its bottom center is at that point.
        """
        screen_x, screen_y = world_to_screen(
            state.player_world_x,
            state.player_world_y,
            camera.x,
            camera.y,
        )

        sprite = self._get_player_sprite(state.facing_direction)
        sprite_rect = sprite.get_rect()

        # Bottom-center of sprite at (screen_x, screen_y - 6) for a tiny visual lift
        draw_x = int(screen_x - sprite_rect.width / 2)
        draw_y = int(screen_y - sprite_rect.height + 6)

        self.screen.blit(sprite, (draw_x, draw_y))

        # ---------- Health bar above player ----------
        ratio = 0.0
        if state.max_health > 0:
            ratio = max(0.0, min(1.0, state.health / state.max_health))

        bar_y = draw_y - HEALTH_BAR_HEIGHT - 4  # a bit above the sprite
        self.health_bar.draw(self.screen, screen_x, bar_y, ratio)

    def _draw_boss(self, state: LocalState, camera: Camera) -> None:
        """
        Draw the chasing boss with a health bar.
        """
        if state.boss is None:
            return

        screen_x, screen_y = world_to_screen(
            state.boss.x,
            state.boss.y,
            camera.x,
            camera.y,
        )

        # Draw damage radius ring (semi-transparent)
        ring_radius = int(BOSS_ATTACK_RANGE)
        ring_size = ring_radius * 2 + 4
        ring_surface = pygame.Surface((ring_size, ring_size), pygame.SRCALPHA)
        pygame.draw.circle(
            ring_surface,
            (255, 0, 0, 90),  # semi-transparent red
            (ring_size // 2, ring_size // 2),
            ring_radius,
            width=2,
        )
        self.screen.blit(
            ring_surface,
            (int(screen_x - ring_size // 2), int(screen_y - ring_size // 2)),
        )

        # Placeholder: draw a colored circle for the boss.
        pygame.draw.circle(
            self.screen,
            COLOR_BOSS,
            (int(screen_x), int(screen_y - 6)),
            18,
        )

        ratio = 0.0
        if state.boss.max_health > 0:
            ratio = max(0.0, min(1.0, state.boss.health / state.boss.max_health))

        bar_y = screen_y - 30
        self.health_bar.draw(self.screen, screen_x, bar_y, ratio)
