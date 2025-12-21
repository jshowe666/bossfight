"""
Input handling:
- quitting
- centering camera
- issuing move commands on right-click
- casting Q (Ezreal-style missile) toward the mouse
"""

from typing import Tuple

import pygame

from shared.game_logic.isometric import screen_to_grid, screen_to_world
from client.game.local_state import LocalState
from client.game.camera import Camera


class InputHandler:
    """
    Handles pygame events and translates them into game actions.
    """

    def process_events(self, state: LocalState, camera: Camera) -> bool:
        """
        Process all pygame events for this frame.
        Returns:
            False if the game should exit, True otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE:
                    # Center camera on player
                    camera.center_on(state.player_world_x, state.player_world_y)
                if event.key == pygame.K_q:
                    self._handle_q_cast(state, camera)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
                mouse_x, mouse_y = event.pos
                target_row, target_col = screen_to_grid(
                    mouse_x,
                    mouse_y,
                    camera.x,
                    camera.y,
                )

                if state.is_walkable(target_row, target_col):
                    state.request_path_to(target_row, target_col)

        return True

    # ---------- Spell casting helpers ----------

    def _handle_q_cast(self, state: LocalState, camera: Camera) -> None:
        """
        Cast Q missile toward the current mouse position (world-space).
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        target_world_x, target_world_y = screen_to_world(
            mouse_x,
            mouse_y,
            camera.x,
            camera.y,
        )
        state.cast_q_spell(target_world_x, target_world_y)
