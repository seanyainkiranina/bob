import os
import pygame
import random
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT


class Game:
    """ Main game class for Irata Warrior. Handles initialization, resource loading, and the main game loop. """
    def __init__(self):
        """ Initialize the game, load resources, and set up the display. """
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Irata Warrior")
        self.clock = pygame.time.Clock()
        self.running = True
        self.playerX = 400
        self.playerY = 550
        self.missleX = 400
        self.missleY = 550
        self.pacmanX = -10
        self.pacmanY = 0
        self.etX = -10
        self.etY = 0
        self.keyboardX = -10
        self.keyboardY = 0
        self.intelliX = -10
        self.intelliY = 0
        self.kongX = -10
        self.kongY = 0
        self.enemyX = 810
        self.enemyY = 0
        self.a5200X = 1000
        self.a5200Y = 0
        self.load_resources()
        self.pacman_shown = False
        self.keyboard_shown = False
        self.intelli_shown = False
        self.kong_shown = False
        self.et_shown = False
        self.enemy_shown = False
        self.a5200_shown = False

    def load_resources(self):
        """  Load images, sounds, and other resources here """
        main_dir = os.path.split(os.path.abspath(__file__))[0]
        data_dir = os.path.join(main_dir, "images")
        self.player = pygame.image.load(os.path.join(data_dir, "player.png"))
        self.player_rect = self.player.get_rect()
        self.missle = pygame.image.load(os.path.join(data_dir, "missle.png"))
        self.missle_rect = self.missle.get_rect()
        self.pacman = pygame.image.load(os.path.join(data_dir, "pacman.png"))
        self.pacman_rect = self.pacman.get_rect()
        self.pacmanY = self.pacman.get_height()
        self.keyboard = pygame.image.load(os.path.join(data_dir, "keyboard.png"))  #
        self.keyboardY = self.pacmanY + self.keyboard.get_height() + 10
        self.keyboard_rect = self.keyboard.get_rect()
        self.intelli = pygame.image.load(os.path.join(data_dir, "intelli.png"))
        self.intelliY = self.keyboardY + self.intelli.get_height() + 10
        self.intelli_rect = self.intelli.get_rect()
        self.kong = pygame.image.load(os.path.join(data_dir, "kong.png"))
        self.kongY = self.intelliY + self.kong.get_height() + 10
        self.kong_rect = self.kong.get_rect()
        self.et = pygame.image.load(os.path.join(data_dir, "et.png"))
        self.etY = self.kongY + self.et.get_height() + 10
        self.et_rect = self.et.get_rect()
        self.enemy = pygame.image.load(os.path.join(data_dir, "enemy.png"))
        self.enemyY = self.etY + self.enemy.get_height() + 30
        self.enemy_rect = self.enemy.get_rect()
        self.a5200 = pygame.image.load(os.path.join(data_dir, "5200.png"))
        self.a5200Y = self.enemyY + 30
        self.a5200_rect = self.a5200.get_rect()
 
    def load_enemy(self):
        """ Load and display enemies and other game elements. """
        random_number = random.randint(1, 100)

        if random_number < 10 and not self.pacman_shown:
            self.pacmanX = 800 + self.pacman.get_width()
            self.pacman_shown = True

        self.screen.blit(self.pacman, (self.pacmanX, self.pacmanY))

        if random_number > 10 and random_number < 20 and not self.keyboard_shown:
            self.keyboardX = 800 + self.keyboard.get_width()
            self.keyboard_shown = True

        self.screen.blit(self.keyboard, (self.keyboardX, self.keyboardY))

        if random_number > 20 and random_number < 30 and not self.intelli_shown:
            self.intelliX = 800 + self.intelli.get_width()
            self.intelli_shown = True

        self.screen.blit(self.intelli, (self.intelliX, self.intelliY))
        if random_number > 30 and random_number < 40 and not self.kong_shown:
            self.kongX = 800 + self.kong.get_width()
            self.kong_shown = True

        self.screen.blit(self.kong, (self.kongX, self.kongY))

        if random_number > 40 and random_number < 50 and not self.et_shown:
            self.etX = 800 + self.et.get_width()
            self.et_shown = True

        self.screen.blit(self.et, (self.etX, self.etY))

        if random_number > 50 and random_number < 60 and not self.enemy_shown:
            self.enemyX = 0 - self.enemy.get_width()
            self.enemy_shown = True

        self.screen.blit(self.enemy, (self.enemyX, self.enemyY))

        if random_number > 60 and random_number < 70 and not self.a5200_shown:
            self.a5200X = 800 + self.a5200.get_width()
            self.a5200_shown = True
        self.screen.blit(self.a5200, (self.a5200X, self.a5200Y))

        if self.a5200_shown and self.a5200X > 0:
            if random_number > 90:
                self.a5200X -= random.randint(0, 5)
        self.screen.blit(self.a5200, (self.a5200X, self.a5200Y))

        if self.a5200X <= 0 and self.a5200_shown:
            self.a5200X = 900
            self.a5200_shown = False

        if self.a5200X >= 1000 and self.a5200_shown:
            self.a5200X = 100
            self.a5200_shown = False

        if self.keyboard_shown and self.keyboardX > 0:
            self.keyboardX -= random.randint(0, 2)
            self.screen.blit(self.keyboard, (self.keyboardX, self.keyboardY))

        if self.intelli_shown and self.intelliX > 0:
            self.intelliX -= random.randint(0, 3)
        self.screen.blit(self.intelli, (self.intelliX, self.intelliY))

        if self.kong_shown and self.kongX > 0:
            self.kongX -= random.randint(0, 1)
        self.screen.blit(self.kong, (self.kongX, self.kongY))

        if self.et_shown and self.etX > 0:
            self.etX -= random.randint(0, 2)
            self.screen.blit(self.et, (self.etX, self.etY))

        if self.pacman_shown and self.pacmanX > 0:
            self.pacmanX -= random.randint(0, 3)
            self.screen.blit(self.pacman, (self.pacmanX, self.pacmanY))

        if self.enemy_shown and self.enemyX < 810:
            self.enemyX += random.randint(0, 3)
            self.screen.blit(self.enemy, (self.enemyX, self.enemyY))

        if self.enemyX >= 800 and self.enemy_shown:
            self.enemyX = -10
            self.enemy_shown = False

        if self.kongX <= 0 and self.kong_shown:
            self.kongX = -10
            self.kong_shown = False

        if self.intelliX <= 0 and self.intelli_shown:
            self.intelliX = -10
            self.intelli_shown = False

        if self.keyboardX <= 0 and self.keyboard_shown:
            self.keyboardX = -10
            self.keyboard_shown = False

        if self.etX <= 0 and self.et_shown:
            self.etX = -10
            self.et_shown = False

        if self.pacmanX <= 0 and self.pacman_shown:
            self.pacmanX = -10
            self.pacman_shown = False
        pygame.display.update()  # Update the display

    def fire_missle(self):
        """ Fire a missile from the player's position. """
        if self.missleY > 0:
            self.missleY = self.missleY - (self.missle.get_height()) - 1
            self.screen.blit(self.missle, (self.missleX, self.missleY))
            #        pygame.display.flip()  # Update the display
            pygame.display.update(self.missle_rect)  # Update the display

    def run(self):
        """ Main game loop. """
        fired = False
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.playerX -= 1
            if keys[pygame.K_RIGHT]:
                self.playerX += 1
            if keys[pygame.K_SPACE]:
                if not fired:
                    self.missleX = (
                        self.playerX
                        + (self.player.get_width() // 2)
                        - (self.missle.get_width() // 2)
                    )
                    fired = True

            if fired:
                self.fire_missle()

            if self.missleY < 0:
                fired = False
                self.missleY = 550

            if self.playerX < 0:
                self.playerX = 0
            if self.playerX > 800 - self.player.get_width():
                self.playerX = 800 - self.player.get_width()

            self.load_enemy()

            self.screen.fill((0, 0, 0))  # Clear the screen with black
            self.clock.tick(60)  # Limit to 60 FPS
            self.screen.blit(self.player, (self.playerX, self.playerY))
            #    pygame.display.flip()  # Update the display
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
