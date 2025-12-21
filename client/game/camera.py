"""
Camera logic for panning around the isometric map.
"""

from shared.constants import EDGE_MARGIN, CAMERA_PAN_SPEED


class Camera:
    """
    Simple 2D camera that stores an offset (x, y) applied to world coordinates
    to produce screen coordinates.
    """

    def __init__(self, screen_width: int, screen_height: int, player_world_x: float, player_world_y: float):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Initialize camera centered on player
        self.x = screen_width / 2 - player_world_x
        self.y = screen_height / 2 - player_world_y

    def center_on(self, world_x: float, world_y: float) -> None:
        """
        Center the camera on the given world position.
        """
        self.x = self.screen_width / 2 - world_x
        self.y = self.screen_height / 2 - world_y

    def update_for_mouse(self, mouse_x: int, mouse_y: int, dt: float) -> None:
        """
        Pan the camera if the mouse is near the edges of the screen.
        """
        # Horizontal pan
        if mouse_x < EDGE_MARGIN:
            self.x += CAMERA_PAN_SPEED * dt  # pan left
        elif mouse_x > self.screen_width - EDGE_MARGIN:
            self.x -= CAMERA_PAN_SPEED * dt  # pan right

        # Vertical pan
        if mouse_y < EDGE_MARGIN:
            self.y += CAMERA_PAN_SPEED * dt  # pan up
        elif mouse_y > self.screen_height - EDGE_MARGIN:
            self.y -= CAMERA_PAN_SPEED * dt  # pan down

        # Optional: clamp the camera here so you don't pan into empty space.
        # For now we leave it unclamped like your original script.
