"""
GameEngine: owns the targets and handles player clicks.

Starter version: a few static targets that respawn elsewhere when
clicked (correctly or not, depending on the hit-detection bug) - no
movement, no score/combo, no timer yet. That's Tasks 2-4.
"""

import random
import time

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
        self.round_duration = 30
        self.time_remaining = self.round_duration
        self.game_over = False
        self.round_start_time = time.time()

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
        if self.game_over:
            return
        
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
        if self.game_over:
            return

        elapsed = time.time() - self.round_start_time
        self.time_remaining = max(0, self.round_duration - elapsed)

        if self.time_remaining <= 0:
            self.time_remaining = 0
            self.game_over = True
            return

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

        renderer.draw_text(
            surface,
            font,
            f"Time: {self.time_remaining:.1f}s",
            (10, 70),
        )

        if self.game_over:
            renderer.draw_text(
                surface,
                font,
                f"TIME'S UP!  Final Score: {self.score}",
                (200, 220),
            )

            renderer.draw_text(
                surface,
                font,
                "Press R to start a new round",
                (180, 250),
            )

    def restart_round(self):
        self.targets = [self._random_target(i) for i in range(NUM_TARGETS)]

        self.hits = 0
        self.misses = 0

        self.score = 0
        self.combo = 0
        self.combo_multiplier = 1

        self.time_remaining = self.round_duration
        self.round_start_time = time.time()
        self.game_over = False