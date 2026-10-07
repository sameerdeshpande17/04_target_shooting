"""
Target: a circular target the player clicks on.
(x, y) is the CENTER of the circle.
"""

import pygame


class Target:
    def __init__(self, x, y, radius=28, color=(230, 90, 70), vx=0, vy=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = vx
        self.vy = vy

    def get_bounding_rect(self):
        """Legacy helper; hit detection uses the real circle."""
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    def update(self, dt, width, height):
        """Move the target and bounce off the play-area edges."""
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = abs(self.vx)

        elif self.x + self.radius >= width:
            self.x = width - self.radius
            self.vx = -abs(self.vx)

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = abs(self.vy)

        elif self.y + self.radius >= height:
            self.y = height - self.radius
            self.vy = -abs(self.vy)