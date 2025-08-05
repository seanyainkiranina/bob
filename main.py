import os
import pygame
import random
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Irata Warrior')
        self.clock = pygame.time.Clock()
        self.running = True
        self.playerX = 400
        self.playerY = 550
        self.missleX = 400
        self.missleY = 550
        self.pacmanX = -10
        self.pacmanY = 0
        self.load_resources()
        self.pacman_shown = False
         
    def load_resources(self):
        # Load images, sounds, and other resources here
        main_dir = os.path.split(os.path.abspath(__file__))[0]
        data_dir = os.path.join(main_dir, "images")
        self.player = pygame.image.load(os.path.join(data_dir, 'player.png'))
        self.missle = pygame.image.load(os.path.join(data_dir, 'missle.png')) 
        self.pacman = pygame.image.load(os.path.join(data_dir, 'pacman.png'))
        self.pacmanY = self.pacman.get_height() #

    def load_enemy(self):
        random_number = random.randint(1, 100)
        if random_number < 50 and not self.pacman_shown:
            self.pacmanX = random.randint(0, 800 - self.pacman.get_width())
            self.pacmanY = self.pacman.get_height()
            self.screen.blit(self.pacman, (self.pacmanX, self.pacmanY))
            self.pacman_shown = True

        if self.pacman_shown and self.pacmanX > 0:
            self.pacmanX -= 1
            self.screen.blit(self.pacman, (self.pacmanX, self.pacmanY))
            pygame.display.flip()

        if self.pacmanX <= 0:
            self.pacmanY = 0
            self.pacmanX = -10
            self.pacman_shown = False



    def fire_missle(self):
            if self.missleY > 0:
                self.missleY =self.missleY - (self.missle.get_height()) - 1
                self.screen.blit(self.missle, (self.missleX, self.missleY))
                pygame.display.flip()  # Update the display
                pygame.display.update()   # Update the display

    def run(self):
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
                    self.missleX = self.playerX + (self.player.get_width() // 2) - (self.missle.get_width() // 2)
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
            pygame.display.flip()  # Update the display
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":  
    game = Game()
    game.run()  