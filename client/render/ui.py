"""
Reusable UI drawing helpers (health bars, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import pygame


@dataclass
class HealthBarRenderer:
    """
    Draws a centered horizontal health bar.
    """

    width: int
    height: int
    bg_color: Tuple[int, int, int]
    fill_color: Tuple[int, int, int]
    border_color: Tuple[int, int, int]

    def draw(self, surface: pygame.Surface, center_x: float, top_y: float, ratio: float) -> None:
        """
        Draw a health bar whose center is at (center_x, top_y + height/2).
        `ratio` should be clamped between 0 and 1.
        """
        ratio = max(0.0, min(1.0, ratio))

        bar_x = int(center_x - self.width / 2)
        bar_y = int(top_y)

        # Background
        pygame.draw.rect(
            surface,
            self.bg_color,
            (bar_x, bar_y, self.width, self.height),
        )

        # Fill
        fill_width = int((self.width - 2) * ratio)
        if fill_width > 0:
            pygame.draw.rect(
                surface,
                self.fill_color,
                (bar_x + 1, bar_y + 1, fill_width, self.height - 2),
            )

        # Border
        pygame.draw.rect(
            surface,
            self.border_color,
            (bar_x, bar_y, self.width, self.height),
            1,
        )
