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
        self._saved_x = 0
        self._saved_y = 0
        self._explosions = []
        self._score = 0
        self._max_score =0

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
            z = random.randint(1, 3)
            if z > 1:
                gallary_target.shown = True
            self._targets.append(gallary_target)
            last_y += gallary_target.height + 10

    def load_enemy(self):
        """Load and display enemies and other game elements."""
        for gallerytarget in self._targets:
            rr = random.randint(1, 100)
            if rr > 75 and gallerytarget.shown:
                self._score += gallerytarget.move_x_target(random.randint(0, 2))

    def kill_enemy(self, missle, target):
        """Check for collision between missile and target."""
        if (
            missle.x < target.x + target.width
            and missle.x + missle.width > target.x
            and missle.y < target.y + target.height
            and missle.y + missle.height > target.y
        ):
            if target.name == "5200":
                missle.y = -10
                return False
            target.shown = False
            self.saved_x = target.x
            self.saved_y = target.y
            target.x = target.explode()
            self_explosions = target.getexploded_images()
            return True
        return False

    def fire_missle(self):
        """Fire a missile from the player's position."""
        if self._missle.y > 0:
            self._missle.move_up()
            self._screen.blit(self._missle.image, (self._missle.x, self._missle.y))

    def run(self):
        """Main game loop."""
        images_shown = 0
        explosion = None
        fired = False
        self._score = 0
        wait = 0
        self._clock.tick(60)  # Limit to 60 FPS
        self._screen.fill((0, 0, 0))  # Clear the screen with black
        font = pygame.font.Font(
            None, 20
        )  # None uses the default font, 36 is the font size
        while self._running:
            if self._max_score < self._score:
                self._max_score = self._score
            self._screen.fill((0, 0, 0))  # Clear the screen with black
            if self._score > -10:
                text = font.render(f"Score:{self._score}", True, (255, 255, 255))  # White text
            else:
                text = font.render(f"Game Over Your Final Score:{self._max_score}", True, (255, 0, 0))
            text_rect = text.get_rect(center=(100, 600 - 20))

            for event in pygame.event.get():
                if event.type == QUIT:
                    self._running = False
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self._player.move_x_player(-1)
            if keys[pygame.K_RIGHT]:
                self._player.move_x_player(1)
            if keys[pygame.K_SPACE]:
                if not fired and self._score > -10:
                    self._missle.x = (
                        self._player.x + self._player.width / 2 - self._missle.width / 2
                    )
                    self._missle.y = self._player.y - self._missle.height - 1
                    fired = True

            if fired:
                self.fire_missle()
                pygame.display.update(self._missle.rect)  # Update the display

            if self._missle.y < 0:
                fired = False
                self._missle.y = 650

            self.load_enemy()
            images_shown = 0
            for gallerytarget in self._targets:
                if gallerytarget.shown:
                    images_shown += 1
                    self._screen.blit(
                        gallerytarget.image, (gallerytarget.x, gallerytarget.y)
                    )
                    if fired:
                        if self.kill_enemy(self._missle, gallerytarget):
                            self._score += 3
                            fired = False
                            self._missle.y = -10
                            self._explosions = gallerytarget.getexploded_images()
                            explosion = self._explosions.pop(0)
                else:
                    if images_shown < 6:
                        zz = random.randint(1, 100)
                        if zz < 50:
                            gallerytarget.shown = True
                            images_shown += 1

            if self._score > -10:
               self._screen.blit(self._player.image, (self._player.x, self._player.y))
            self._screen.blit(text, text_rect)
            if explosion is not None:
                self._screen.blit(explosion, (self.saved_x, self.saved_y))

            if explosion is not None and wait > 10:
                if len(self._explosions) > 0:
                    explosion = self._explosions.pop(0)
                else:
                    explosion = None
                wait = 0
            if explosion is not None:
                wait += 1

            pygame.display.update()

        pygame.display.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
