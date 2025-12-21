"""
Entry point for the local single-player isometric prototype.

This reproduces your monolithic example:
- fullscreen at monitor resolution
- large isometric grid
- water patches as obstacles
- camera panning when the mouse hits the screen edges
- right-click pathfinding using Dijkstra
- SPACE to center camera on the player
"""

import pygame

from shared.constants import (
    DEFAULT_GRID_ROWS,
    DEFAULT_GRID_COLS,
)
from client.game.local_state import LocalState
import client.game.camera as camera_module
from client.game.input_handler import InputHandler
from client.render.renderer import Renderer


def main() -> None:
    pygame.init()

    # Get the actual monitor resolution (e.g., 3440x1440)
    info = pygame.display.Info()
    # screen_width = info.current_w
    # screen_height = info.current_h

    screen_width = 1600
    screen_height = 900

    screen = pygame.display.set_mode(

        (screen_width, screen_height),
        pygame.RESIZABLE
    )
    pygame.display.set_caption("Isometric RTS Prototype")

    clock = pygame.time.Clock()

    # --- Game objects ---
    state = LocalState(
        rows=DEFAULT_GRID_ROWS,
        cols=DEFAULT_GRID_COLS,
        water_patches=80,
        rng_seed=1,
    )

    camera = camera_module.Camera(
        screen_width=screen_width,
        screen_height=screen_height,
        player_world_x=state.player_world_x,
        player_world_y=state.player_world_y,
    )

    renderer = Renderer(screen, screen_width, screen_height)
    input_handler = InputHandler()

    running = True

    while running:
        dt = clock.tick(60) / 1000.0  # seconds

        # Handle input / events
        running = input_handler.process_events(state, camera)
        if not running:
            break

        # Camera panning (mouse at edges)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        camera.update_for_mouse(mouse_x, mouse_y, dt)
        if input_handler.center_on_player:
            camera.center_on(state.player_world_x, state.player_world_y)

        # Update world (player movement along path)
        state.update(dt)

        # Render
        renderer.render(state, camera)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
