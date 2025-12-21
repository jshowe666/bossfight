"""
Global constants shared between client and server.
These define core parameters such as tile size, map dimensions,
camera behavior, colors, etc.
"""

# -------- TILE GEOMETRY (isometric) --------
TILE_WIDTH = 16       # pixel width of an isometric tile
TILE_HEIGHT = 8      # pixel height of an isometric tile

# -------- MAP SIZE (defaults; client can override for fullscreen) --------
DEFAULT_GRID_ROWS = 100
DEFAULT_GRID_COLS = 100

# -------- CAMERA --------
EDGE_MARGIN = 30           # px from edge that triggers panning
CAMERA_PAN_SPEED = 1800.0  # px per second

# -------- MOVEMENT --------
PLAYER_MOVE_SPEED = 500.0  # world px / second

# -------- SPELLS / PROJECTILES --------
# Ezreal-Q-style missile
Q_MISSILE_SPEED = 900.0      # world px / second
Q_MISSILE_RANGE = 1000.0     # max distance before despawn
Q_MISSILE_RADIUS = 4         # pixels (for drawing)
Q_COOLDOWN = 1.0             # seconds

# -------- COLORS --------
COLOR_BACKGROUND = (30, 30, 30)
COLOR_LAND = (34, 139, 34)
COLOR_WATER = (30, 144, 255)
COLOR_PATH = (255, 255, 0)
COLOR_PLAYER = (220, 20, 60)

# Projectiles (light blue-ish, stands out)
COLOR_Q_MISSILE = (135, 206, 250)

# -------- PLAYER HEALTH --------
MAX_PLAYER_HEALTH = 100

HEALTH_BAR_WIDTH = 40
HEALTH_BAR_HEIGHT = 6

COLOR_HEALTH_BG = (60, 60, 60)        # bar background
COLOR_HEALTH_FILL = (46, 204, 113)    # green health
COLOR_HEALTH_BORDER = (0, 0, 0)       # outline

