"""
GameEngine: owns the targets and handles player clicks.

Starter version: a few static targets that respawn elsewhere when
clicked (correctly or not, depending on the hit-detection bug) - no
movement, no score/combo, no timer yet. That's Tasks 2-4.
"""

import random

from game import renderer
from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28


class GameEngine:
    def __init__(self):
        self.targets = [self._random_target(i) for i in range(NUM_TARGETS)]
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.combo = 0
        self.combo_multiplier = 1
        self.points_per_hit = 10

    def _random_target(self, index=0):
        x = random.randint(TARGET_RADIUS + 10, WIDTH - TARGET_RADIUS - 10)
        y = random.randint(TARGET_RADIUS + 10, HEIGHT - TARGET_RADIUS - 10)

        speeds = [
            (120, 80),
            (-160, 100),
            (100, -140),
        ]

        vx, vy = speeds[index % len(speeds)]

        return Target(
            x,
            y,
            radius=TARGET_RADIUS,
            vx=vx,
            vy=vy,
        )

    def handle_click(self, pos):
        target = check_hit(self.targets, pos)

        if target is not None:
            self.hits += 1

            self.combo += 1
            self.combo_multiplier = self.combo

            self.score += self.points_per_hit * self.combo_multiplier

            self.targets.remove(target)
            self.targets.append(self._random_target(len(self.targets)))

        else:
            self.misses += 1

            self.combo = 0
            self.combo_multiplier = 1

    def update(self, dt):
        for target in self.targets:
            target.update(dt, WIDTH, HEIGHT)

    def draw(self, surface, font):
        renderer.draw_scene(surface, self.targets)

        renderer.draw_text(
            surface,
            font,
            f"Hits: {self.hits}  Misses: {self.misses}",
            (10, 10),
        )

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}  Combo: {self.combo_multiplier}x",
            (10, 40),
        )
