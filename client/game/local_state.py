"""
Local game state for the client:
- grid (land/water)
- player position (grid + world)
- current path and movement along it
- active missiles (Ezreal-Q-style projectiles)
- facing direction (for directional sprites)
"""

from typing import List, Tuple, Optional

from shared.constants import (
    DEFAULT_GRID_ROWS,
    DEFAULT_GRID_COLS,
    PLAYER_MOVE_SPEED,
    Q_MISSILE_SPEED,
    Q_MISSILE_RANGE,
    Q_COOLDOWN,
    MAX_PLAYER_HEALTH,
    BOSS_MOVE_SPEED,
    BOSS_MAX_HEALTH,
    BOSS_ATTACK_RANGE,
    BOSS_DAMAGE_PER_SECOND,
    BOSS_HIT_RADIUS,
    Q_MISSILE_DAMAGE,
)
from shared.game_logic.isometric import grid_to_world
from shared.game_logic.map_generation import create_grid, generate_water_patches
from shared.game_logic.pathfinding import dijkstra
from shared.game_models import Missile, Boss


Grid = List[List[int]]
Cell = Tuple[int, int]


class LocalState:
    """
    Encapsulates the local game state on the client:
    - Terrain grid
    - Player position
    - Current movement path
    - Active missiles
    - Spell cooldowns
    - Facing direction for the player sprite
    """

    def __init__(
        self,
        rows: int = DEFAULT_GRID_ROWS,
        cols: int = DEFAULT_GRID_COLS,
        water_patches: int = 120,
        rng_seed: Optional[int] = 1,
    ):
        # --- Grid setup ---
        self.grid_rows = rows
        self.grid_cols = cols

        self.grid: Grid = create_grid(rows, cols, seed=rng_seed)
        generate_water_patches(
            self.grid,
            num_patches=water_patches,
            min_size=5,
            max_size=20,
        )

        # --- Player setup (starts at (0, 0)) ---
        self.player_row: int = 0
        self.player_col: int = 0
        self.player_world_x, self.player_world_y = grid_to_world(
            self.player_row, self.player_col
        )

        # Facing direction for sprite: "up", "down", "left", "right"
        self.facing_direction: str = "down"

        # --- Health ---
        self.max_health: int = MAX_PLAYER_HEALTH
        self.health: int = self.max_health

        # --- Movement/path state ---
        self.current_path: List[Cell] = []
        self.path_index: int = 0

        # --- Projectiles (Ezreal Q) ---
        self.missiles: List[Missile] = []

        # --- Cooldowns ---
        self.q_cooldown_remaining: float = 0.0

        # --- Boss ---
        self.boss: Optional[Boss] = self._spawn_boss()
        self.boss_path: List[Cell] = []
        self.boss_path_index: int = 0

    # ---------- Path / movement logic ----------

    def request_path_to(self, target_row: int, target_col: int) -> None:
        """
        Compute a new path from the player's current tile to (target_row, target_col).
        If no path exists, the current path is cleared.
        """
        start = (self.player_row, self.player_col)
        goal = (target_row, target_col)

        path = dijkstra(self.grid, start, goal)
        if path:
            self.current_path = path
            self.path_index = 0
        else:
            self.current_path = []
            self.path_index = 0

    def _update_facing_direction(self, next_row: int, next_col: int) -> None:
        """
        Update facing_direction based on the *grid* movement direction.

        We look at the delta (dr, dc) in grid coordinates and map the 8 possible
        directions to 4 cardinal facings (up, down, left, right) in a way that
        feels correct in isometric view.
        """
        dr = next_row - self.player_row
        dc = next_col - self.player_col

        if dr == 0 and dc == 0:
            return

        # Cardinal directions
        if dr < 0 and dc == 0:  # North
            self.facing_direction = "up"
        elif dr > 0 and dc == 0:  # South
            self.facing_direction = "down"
        elif dr == 0 and dc < 0:  # West
            self.facing_direction = "left"
        elif dr == 0 and dc > 0:  # East
            self.facing_direction = "right"

        # Diagonals
        elif dr < 0 and dc < 0:  # North-West
            self.facing_direction = "up"
        elif dr < 0 and dc > 0:  # North-East
            self.facing_direction = "right"
        elif dr > 0 and dc < 0:  # South-West
            self.facing_direction = "left"
        elif dr > 0 and dc > 0:  # South-East
            self.facing_direction = "down"

    def _update_player_movement(self, dt: float) -> None:
        """
        Advance the player's movement along the current path based on dt (seconds).
        Movement is in world-space (smooth movement between tiles).
        Also updates facing_direction when we start moving toward a new tile.
        """
        if not self.current_path or self.path_index >= len(self.current_path) - 1:
            return

        # Next grid cell along the path
        next_row, next_col = self.current_path[self.path_index + 1]

        # Update facing direction based on which way we're heading
        self._update_facing_direction(next_row, next_col)

        next_world_x, next_world_y = grid_to_world(next_row, next_col)

        dx = next_world_x - self.player_world_x
        dy = next_world_y - self.player_world_y

        dist = (dx * dx + dy * dy) ** 0.5
        if dist <= 0.0:
            return

        step = PLAYER_MOVE_SPEED * dt

        if step >= dist:
            # Snap to tile center
            self.player_world_x = next_world_x
            self.player_world_y = next_world_y
            self.player_row, self.player_col = next_row, next_col
            self.path_index += 1
        else:
            # Partial movement toward the next tile
            self.player_world_x += dx / dist * step
            self.player_world_y += dy / dist * step

    def _update_boss_movement(self, dt: float) -> None:
        """
        Move the boss toward the player's current tile using pathfinding.
        """
        if self.boss is None:
            return

        target = (self.player_row, self.player_col)
        if (not self.boss_path or
                self.boss_path_index >= len(self.boss_path) - 1 or
                self.boss_path[-1] != target):
            self._recompute_boss_path(target)

        if not self.boss_path or self.boss_path_index >= len(self.boss_path) - 1:
            return

        next_row, next_col = self.boss_path[self.boss_path_index + 1]
        next_world_x, next_world_y = grid_to_world(next_row, next_col)

        dx = next_world_x - self.boss.x
        dy = next_world_y - self.boss.y

        dist = (dx * dx + dy * dy) ** 0.5
        if dist <= 0.0:
            return

        step = BOSS_MOVE_SPEED * dt
        if step >= dist:
            self.boss.x = next_world_x
            self.boss.y = next_world_y
            self.boss.row, self.boss.col = next_row, next_col
            self.boss_path_index += 1
        else:
            self.boss.x += dx / dist * step
            self.boss.y += dy / dist * step

    def _recompute_boss_path(self, target: Cell) -> None:
        if self.boss is None:
            return

        start = (self.boss.row, self.boss.col)
        path = dijkstra(self.grid, start, target)
        if path:
            self.boss_path = path
            self.boss_path_index = 0
        else:
            self.boss_path = []
            self.boss_path_index = 0

    # ---------- Spells / missiles ----------

    def _direction_from_vector(self, dx: float, dy: float) -> str:
        """
        Map a world-space vector (dx, dy) to a cardinal direction string
        for sprite selection: 'up', 'down', 'left', 'right'.

        We base this on which axis has larger magnitude, and use screen-like
        logic (y+ = down).
        """
        if abs(dx) < 1e-4 and abs(dy) < 1e-4:
            return self.facing_direction  # fall back to current facing

        if abs(dx) >= abs(dy):
            # Horizontal dominates
            return "right" if dx > 0 else "left"
        else:
            # Vertical dominates
            return "down" if dy > 0 else "up"

    def cast_q_spell(self, target_world_x: float, target_world_y: float) -> bool:
        """
        Cast an Ezreal-Q-style missile toward a world-space target.
        Returns True if a missile was created (i.e., not on cooldown & valid dir).
        """
        if self.q_cooldown_remaining > 0.0:
            return False

        start_x = self.player_world_x
        start_y = self.player_world_y

        dx = target_world_x - start_x
        dy = target_world_y - start_y
        dist = (dx * dx + dy * dy) ** 0.5

        if dist <= 0.0001:
            # Mouse basically on top of player, abort
            return False

        # Normalize direction
        vx = dx / dist
        vy = dy / dist

        direction = self._direction_from_vector(vx, vy)

        missile = Missile(
            x=start_x,
            y=start_y,
            vx=vx,
            vy=vy,
            speed=Q_MISSILE_SPEED,
            max_distance=Q_MISSILE_RANGE,
            direction=direction,
        )
        self.missiles.append(missile)

        # Put Q on cooldown
        self.q_cooldown_remaining = Q_COOLDOWN
        return True

    def _update_missiles(self, dt: float) -> None:
        """
        Move missiles forward and despawn them when they reach max range.
        """
        for missile in self.missiles:
            if not missile.active:
                continue

            # Move
            dx = missile.vx * missile.speed * dt
            dy = missile.vy * missile.speed * dt

            missile.x += dx
            missile.y += dy
            step_dist = (dx * dx + dy * dy) ** 0.5
            missile.traveled += step_dist

            if missile.traveled >= missile.max_distance:
                missile.active = False
                continue

            # Boss collision
            if self.boss is not None:
                bdx = missile.x - self.boss.x
                bdy = missile.y - self.boss.y
                if (bdx * bdx + bdy * bdy) <= (BOSS_HIT_RADIUS * BOSS_HIT_RADIUS):
                    self._damage_boss(Q_MISSILE_DAMAGE)
                    missile.active = False

        # Clean up inactive missiles
        self.missiles = [m for m in self.missiles if m.active]

    def _update_cooldowns(self, dt: float) -> None:
        """
        Update spell cooldown timers.
        """
        if self.q_cooldown_remaining > 0.0:
            self.q_cooldown_remaining = max(
                0.0, self.q_cooldown_remaining - dt
            )

    def _update_boss_damage(self, dt: float) -> None:
        """
        Apply boss damage to the player if within range.
        """
        if self.boss is None:
            return

        dx = self.boss.x - self.player_world_x
        dy = self.boss.y - self.player_world_y
        dist_sq = dx * dx + dy * dy
        if dist_sq <= BOSS_ATTACK_RANGE * BOSS_ATTACK_RANGE:
            self.health = max(0.0, self.health - BOSS_DAMAGE_PER_SECOND * dt)

    # ---------- Frame update ----------

    def update(self, dt: float) -> None:
        """
        Called once per frame:
        - update player movement
        - update missiles
        - update cooldowns
        """
        self._update_player_movement(dt)
        self._update_missiles(dt)
        self._update_cooldowns(dt)
        self._update_boss_movement(dt)
        self._update_boss_damage(dt)

    # ---------- Helpers ----------

    def is_walkable(self, row: int, col: int) -> bool:
        """
        Return True if (row, col) is inside the grid and is land (0).
        """
        if not (0 <= row < self.grid_rows and 0 <= col < self.grid_cols):
            return False
        return self.grid[row][col] == 0

    # ---------- Boss helpers ----------

    def _spawn_boss(self) -> Optional[Boss]:
        """
        Place the boss somewhere along the bottom row (searching upward if blocked).
        """
        bottom_row = self.grid_rows - 1
        start_col = self.grid_cols // 2

        for row in range(bottom_row, -1, -1):
            for col in range(start_col, self.grid_cols):
                if self.is_walkable(row, col):
                    world_x, world_y = grid_to_world(row, col)
                    return Boss(
                        row=row,
                        col=col,
                        x=world_x,
                        y=world_y,
                        speed=BOSS_MOVE_SPEED,
                        health=BOSS_MAX_HEALTH,
                        max_health=BOSS_MAX_HEALTH,
                    )
            for col in range(start_col - 1, -1, -1):
                if self.is_walkable(row, col):
                    world_x, world_y = grid_to_world(row, col)
                    return Boss(
                        row=row,
                        col=col,
                        x=world_x,
                        y=world_y,
                        speed=BOSS_MOVE_SPEED,
                        health=BOSS_MAX_HEALTH,
                        max_health=BOSS_MAX_HEALTH,
                    )
        return None

    def _damage_boss(self, amount: float) -> None:
        if self.boss is None:
            return

        self.boss.health = max(0.0, self.boss.health - amount)
        if self.boss.health <= 0.0:
            self.boss = None
            self.boss_path = []
            self.boss_path_index = 0
