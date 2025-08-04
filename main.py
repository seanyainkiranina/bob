import pygame
from pygame.locals import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Irata Warrior')
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))  # Clear the screen with black
            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Limit to 60 FPS

        pygame.quit()

if __name__ == "__main__":  
    game = Game()
    game.run()  