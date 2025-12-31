"""
Camera logic for panning around the isometric map.
"""

from shared.constants import EDGE_MARGIN, CAMERA_PAN_SPEED


class Camera:
    """
    Simple 2D camera that stores an offset (x, y) applied to world coordinates
    to produce screen coordinates.
    """

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        player_world_x: float,
        player_world_y: float,
        world_bounds: tuple,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.min_world_x, self.max_world_x, self.min_world_y, self.max_world_y = world_bounds

        # Initialize camera centered on player
        self.x = screen_width / 2 - player_world_x
        self.y = screen_height / 2 - player_world_y
        self._clamp_to_bounds()

    def center_on(self, world_x: float, world_y: float) -> None:
        """
        Center the camera on the given world position.
        """
        self.x = self.screen_width / 2 - world_x
        self.y = self.screen_height / 2 - world_y
        self._clamp_to_bounds()

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

        self._clamp_to_bounds()

    def _clamp_to_bounds(self) -> None:
        """
        Clamp camera offsets so the view never scrolls beyond the board edges.
        """
        min_cam_x = self.screen_width - self.max_world_x
        max_cam_x = -self.min_world_x
        min_cam_y = self.screen_height - self.max_world_y
        max_cam_y = -self.min_world_y

        # If the map is smaller than the viewport, lock to the center.
        if min_cam_x > max_cam_x:
            self.x = (min_cam_x + max_cam_x) / 2
        else:
            self.x = max(min(self.x, max_cam_x), min_cam_x)

        if min_cam_y > max_cam_y:
            self.y = (min_cam_y + max_cam_y) / 2
        else:
            self.y = max(min(self.y, max_cam_y), min_cam_y)
