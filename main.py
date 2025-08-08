import os
import sys
import random
import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)  # pylint: disable=[E0611,W0611]


sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from target import Target  # type: ignore # Importing Target class from target module


class Game:
    """Handles initialization, resource loading, and the main game loop."""

    def __init__(self):
        """Initialize the game, load resources, and set up the display."""
        pygame.init()
        self._screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Irata Warrior")
        self._clock = pygame.time.Clock()
        self._targets = []
        self._running = True
        self.load_resources()

    def load_resources(self):
        """Load images, sounds, and other resources here"""
        self._player = Target("player", 400, 550, 780, 20)
        self._missle = Target("missle", 400, 610)

        filenames = ["pacman", "keyboard", "intelli", "kong", "et", "enemy", "5200"]
        last_y = 20
        x = -10
        for filename in filenames:
            r = random.randint(1, 100)
            if r < 50:
                x = 810
            else:
                x = -10
            gallary_target = Target(filename, x, last_y)
            self._targets.append(gallary_target)
            last_y += gallary_target.height + 10

    def load_enemy(self):
        """Load and display enemies and other game elements."""
        for gallerytarget in self._targets:
            rr = random.randint(1, 100)
            if rr > 75:

                gallerytarget.move_x_target(random.randint(0, 2))
                self._screen.blit(gallerytarget.image, (gallerytarget.x, gallerytarget.y))
                pygame.display.update(gallerytarget.rect)  # Update the display

        pygame.display.update()  # Update the display

    def fire_missle(self):
        """Fire a missile from the player's position."""
        if self._missle.y > 0:
            self._missle.move_up()
            self._screen.blit(self._missle.image, (self._missle.x, self._missle.y))
            pygame.display.update(self._missle.rect)  # Update the display

    def run(self):
        """Main game loop."""
        fired = False
        self._clock.tick(60)  # Limit to 60 FPS
        self._screen.fill((0, 0, 0))  # Clear the screen with black
        while self._running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self._running = False
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self._player.move_x_player(-1)
            if keys[pygame.K_RIGHT]:
                self._player.move_x_player(1)
            if keys[pygame.K_SPACE]:
                if not fired:
                    self._missle.x = (
                        self._player.x + self._player.width / 2 - self._missle.width / 2
                    )
                    self._missle.y = self._player.y - self._missle.height - 1
                    fired = True

            if fired:
                self.fire_missle()

            if self._missle.y < 0:
                fired = False
                self._missle.y = 650

            self.load_enemy()

            self._screen.fill((0, 0, 0))  # Clear the screen with black
            self._screen.blit(self._player.image, (self._player.x, self._player.y))
            # pygame.display.flip()  # Update the display
            # pygame.display.update(self._player.rect)  # Update the display
            pygame.display.update()

        pygame.display.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
