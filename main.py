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
from score import Score  # pyright: ignore[reportMissingImports]
from state import State  # pyright: ignore[reportMissingImports]


class Game:
    """Handles initialization, resource loading, and the main game loop."""

    def __init__(self):
        """Initialize the game, load resources, and set up the display."""
        pygame.init()
        self._screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Irata Warrior")
        self._clock = pygame.time.Clock()
        self._targets = []
        self._fleas = []
        self._running = True
        self._starting = True
        self.load_resources()
        self._saved_x = 0
        self._saved_y = 0
        self._explosions = []
        self._score = 0
        self._max_score = 0
        self._bombs = []
        self._game_over_images = []
        self._score_board = Score()
        self._font = None
        self._sound = None
        self._fire_sound = None
        self._target_hit_sound = None
        self._game_over_sound = None
        self._saved_x = 0
        self._saved_y = 0
        self._state = State()
        self._counter_5200 = 1

    def load_fleas(self):
        """load fleas here"""
        if len(self._fleas) > 0:
            return
        filenames = [
            "vic20",
            "5200c",
            "nes",
            "odyssey",
            "colecovision",
            "intellivison",
            "chickenlips",
            "luigi",
            "fruit",
            "vectrex",
            "zx",
            "5150",
            "coco",
            "emerson",
        ]
        random.shuffle(filenames)
        y = 0 - random.randint(10, 20)
        lastx = 0
        for filename in filenames:
            y = 0 - random.randint(10, 20)
            gallery_target = Target(filename, lastx, y)
            lastx += gallery_target.width + 10
            gallery_target.shown = True
            gallery_target.nodeduction = True
            self._fleas.append(gallery_target)

    def load_resources(self):
        """Load images, sounds, and other resources here"""
        self.load_fleas()
        self._player = Target("player", 400, 550, 780, 20)
        self._missle = Target("missle", 400, 610)
        filenames = [
            "pacman",
            "keyboard",
            "intelli",
            "kong",
            "et",
            "enemy",
            "5200",
            "ghost1",
            "ghost2",
            "ghost3",
            "ghost4",
        ]
        last_y = 20
        random.shuffle(filenames)
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
            if (
                filename != "ghost1"
                and filename != "ghost2"
                and filename != "ghost3"
                and filename != "ghost4"
            ):
                gallary_target.nodeduction = True
                last_y += gallary_target.height + 10
            if gallary_target.nodeduction:
                if gallary_target.x < 0:
                    gallary_target.x -= gallary_target.width
                else:
                    gallary_target.x += gallary_target.width

    def load_enemy(self):
        """Load and display enemies and other game elements."""
        speed = int(round((self._max_score + 1) / 100, 0)) + 1
        if self._max_score > 999:
            speed = (
                int(round((self._max_score + 1) / 1000, 0))
                + random.randint(0, round(speed / 2))
                + 2
            )
        if self._max_score > 9999:
            speed = (
                int(round((self._max_score + 1) / 10000, 0))
                + random.randint(0, round(speed / 2))
                + 3
            )
        if speed < 1:
            speed = 1
        speed = random.randint(0, speed // 2)
        for gallerytarget in self._targets:
            rr = random.randint(1, 100)
            if rr > 75 and gallerytarget.shown:
                deduction = gallerytarget.move_x_target(random.randint(0, speed))
                if self._score > 19:
                    deduction = deduction * round((self._score / 10), 1)
                self._score += deduction

    def debris_player(self, debris, player):
        """Check for collision between debris and player."""
        if (
            debris.x < player.x + player.width
            and debris.x + debris.width > player.x
            and debris.y < player.y + player.height
            and debris.y + debris.height > player.y
        ):
            return True
        return False

    def flea_player(self, flea, player):
        """Check for collision between flea and player."""
        if (
            flea.x < player.x + player.width
            and flea.x + flea.width > player.x
            and flea.y < player.y + player.height
            and flea.y + flea.height > player.y
        ):
            return True
        return False

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
                self._counter_5200 += 1
                self._score -= self._counter_5200
                if self._score < -10:
                    self.render_score()
                    self.game_over()
                if self._counter_5200 > 2:
                    self._counter_5200 = 1
                return False
            target.shown = False
            self._saved_x = target.x
            self._saved_y = target.y
            target.x = target.explode()
            self._explosions = target.getexploded_images()
            return True
        return False

    def fire_missle(self):
        """Fire a missile from the player's position."""
        if self._missle.y > 0:
            self._missle.move_up()
            self._screen.blit(self._missle.image, (self._missle.x, self._missle.y))

    def instructions(self):
        """load the instructions list"""
        instruct = []
        instruct.append("Welcome To Irata Warrior")
        instruct.append("Space bar to fire and arrows to move left and right")
        instruct.append("Game ends when score is 10 below zero")
        instruct.append("Points are lost when a target scrolls of the screen, ")
        instruct.append("upon debris impact, the controller, or a ghost is shot.")
        instruct.append("Esc to exit")

        return instruct

    def display_instructions(self, start_y, linstructions):
        """display the instruction list"""
        self._counter_5200 = 1
        display_instuct = []
        self._font = pygame.font.Font(
            "lib\\PressStart2P-vaV7.ttf", 11
        )  # None uses the default font, 36 is the font size
        for i in linstructions:
            t = {}
            if i.split(" ")[1] == str(self._max_score):
                t["text"] = self._font.render(i, True, (255, 0, 0))
            else:
                t["text"] = self._font.render(i, True, (255, 255, 255))

            t["text_rect"] = t["text"].get_rect(topleft=(10, start_y))
            start_y += 16
            display_instuct.append(t)
        return display_instuct

    def flea_movement(self):
        """flea movement"""
        for flea in self._fleas:
            if flea.shown:
                if self.flea_player(flea, self._player):
                    self._score -= 1 + (abs(self._score + 1) // 2)
                    flea.shown = False
                    flea.y = 0 - random.randint(10, 20)

    def exploded_target(self):
        """explode a target"""
        bombs_to_remove = []
        fleas_to_remove = []
        if self._state.explosion is not None and self._state.wait > 10:
            if len(self._explosions) > 0:
                self._state.explosion = self._explosions.pop(0)
            else:
                self._state.explosion = None
            self._state.wait = 0
        if self._state.explosion is not None:
            self._state.wait += 1

        for bomb in self._bombs:
            self._screen.blit(bomb.getimage(), (bomb.x, bomb.y))
            bomb.y += 1
            if bomb.last == 0:
                bomb.last = random.randint(-2, 2)
            bomb.x += bomb.last
            for gallerytarget in self._targets:
                if gallerytarget.shown:
                    if self.kill_enemy(bomb, gallerytarget):
                        bombs_to_remove.append(bomb)
                        gallerytarget.shown = False
                        self._state.images_shown -= 1
                        if self._score > -1:
                            self._score += (
                                random.randint(1, (round(bomb.y / 3) + 10))
                                * self._state.bonus
                            )
                        for b in gallerytarget.get_bomb(bomb.x):
                            if len(self._bombs) < random.randint(2, 15):
                                self._bombs.append(b)
        for bomb in self._bombs:
            for flea in self._fleas:
                if flea.shown:
                    if self.kill_enemy(bomb, flea):
                        bombs_to_remove.append(bomb)
                        flea.shown = False
                        fleas_to_remove.append(flea)
                    if self.kill_enemy(self._missle, flea):
                        self._state.shots_fired = 0
                        self._target_hit_sound.play()
                        flea.shown = False
                        self._score += 10
                        fleas_to_remove.append(flea)

            if self.kill_enemy(self._missle, bomb):
                self._score += 1 + self._score
                bombs_to_remove.append(bomb)
            else:
                if self.debris_player(bomb, self._player):
                    self._score -= 1 + self._score
                    bombs_to_remove.append(bomb)
            if bomb.y > 600:
                bombs_to_remove.append(bomb)
        for bomb in bombs_to_remove:
            if bomb in self._bombs:
                self._bombs.remove(bomb)
        for flea in fleas_to_remove:
            if flea in self._fleas:
                self._fleas.remove(flea)

    def run(self):
        """load screen"""
        pygame.mixer.init()
        if self._sound is None:
            self._sound = pygame.mixer.Sound("lib\\BeepBox-Song.wav")
            self._sound.play(1, 1700)

        if self._fire_sound is None:
            self._fire_sound = pygame.mixer.Sound("lib\\fire.mp3")

        if self._target_hit_sound is None:
            self._target_hit_sound = pygame.mixer.Sound("lib\\explosion.mp3")

        if self._game_over_sound is None:
            self._game_over_sound = pygame.mixer.Sound("lib\\nuclear-explosion.mp3")

        self._screen.fill((0, 0, 0))  # Clear the screen with black
        self._font = pygame.font.Font(
            "lib\\PressStart2P-vaV7.ttf", 12
        )  # None uses the default font, 36 is the font size
        if self._max_score > 0:
            self._score_board.value = self._max_score
            self._score_board.save()
        high_scores = self._score_board.get_scores()

        while self._starting:
            instruction_messages = []
            instruction_messages = self.instructions()
            if self._max_score > 0:
                instruction_messages.append(f"Your Score:{self._max_score}")
            if len(high_scores) > 0:
                instruction_messages.append("High Scores")
            for h in high_scores:
                instruction_messages.append(h)
            instruction_messages.append("Points for targets are random,")
            instruction_messages.append(
                "with the most points given for smaller size or distant items."
            )
            instruction_messages.append("S to Start")

            text_messages = self.display_instructions(10, instruction_messages)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self._starting = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                self._starting = False
                self._running = True
            if keys[pygame.K_ESCAPE]:
                self._starting = False
                self._running = True

            for t in text_messages:
                self._screen.blit(t["text"], t["text_rect"])

            pygame.display.update()

        if self._running:
            self.start()

        pygame.display.quit()

    def render_score(self):
        """Show score"""
        if self._max_score < self._score:
            self._max_score = self._score
        self._screen.fill((0, 0, 0))  # Clear the screen with black
        self._score = round(self._score, 1)
        if self._state.last != self._score:
            self._state.difference = round(self._score - self._state.last, 1)
        self._state.last = self._score
        self._max_score = round(self._max_score, 1)
        if self._score > -10:
            text = self._font.render(
                f"Score:{self._score}", True, (255, 255, 255)
            )  # White text
        else:
            text = self._font.render(f"Score:{self._max_score}", True, (255, 0, 0))
        text_rect = text.get_rect(topleft=(10, 600 - 20))
        text_r = self._font.render(
            f"Points:{self._state.difference}", True, (255, 0, 0)
        )

        text_right = text.get_rect(topleft=(600, 600 - 20))
        self._screen.blit(text, text_rect)
        self._screen.blit(text_r, text_right)

    def game_over(self):
        """game over"""
        if self._score < -9 and not self._state.game_over_done:
            self._state.game_over_wait += 1
            self._state.end_started += 1

        if self._state.end_started == 1:
            self._game_over_sound.play()

        if (
            self._score < -9
            and len(self._game_over_images) == 0
            and not self._state.game_over_done
        ):
            self._state.fired = True
            self._game_over_images = self._player.get_game_over_images()
            self._state.game_over_wait = 10001

        if (
            self._score < -9
            and (self._state.game_over_wait > 99)
            and len(self._game_over_images) > 0
            and not self._state.game_over_done
        ):
            self._state.fired = True
            self._state.game_over_image = self._game_over_images.pop(0)
            self._screen.blit(
                self._state.game_over_image, (self._player.x, self._player.y - 50)
            )
            self._state.game_over_wait = 1
            if len(self._game_over_images) == 0:
                self._running = False
                self._state.game_over_done = True
        else:
            if len(self._game_over_images) == 0 and self._score < -9:
                self._state.game_over_done = True

        if self._state.game_over_wait > 0 and not self._state.game_over_done:
            self._screen.blit(
                self._state.game_over_image, (self._player.x, self._player.y - 50)
            )

    def target_movement(self):
        """target movement"""
        r = random.randrange(1, 300)
        if len(self._fleas) == 0:
            self.load_fleas()
        for flea in self._fleas:
            if flea.shown:
                if random.randint(1, 100) > 50:
                    flea.y += 1
                self._screen.blit(flea.image, (flea.x, flea.y))
                if flea.y > 600:
                    flea.shown = False
            else:
                zz = random.randint(1, 100)
                if zz < 50:
                    flea.shown = True
                    flea.x = random.randint(10, 580)
                    flea.y = 0 - random.randint(10, 200)
        for flea in self._fleas:
            if flea.shown:
                if self._state.fired and self._score > -9:
                    if self.kill_enemy(self._missle, flea):
                        self._state.fired = False
                        self._state.shots_fired = 0
                        self._target_hit_sound.play()
                        flea.shown = False
                        self._score += 10

        for gallerytarget in self._targets:
            if gallerytarget.shown:
                self._state.images_shown += 1
                self._screen.blit(
                    gallerytarget.image, (gallerytarget.x, gallerytarget.y)
                )
                self._state.last_x = gallerytarget.x + gallerytarget.width / 2
                if self._state.fired and self._score > -9:
                    if self.kill_enemy(self._missle, gallerytarget):
                        self._state.shots_fired = 0
                        self._target_hit_sound.play()
                        if gallerytarget.nodeduction:
                            if self._max_score < r:
                                if self._score > -9:
                                    self._score += (
                                        103 - gallerytarget.width
                                    ) * self._state.bonus
                            else:
                                if self._score > -9:
                                    self._score += (
                                        (600 - gallerytarget.y) / 100
                                    ) * self._state.bonus
                            self._score -= (abs(self._score) + 1) / 4
                        self._state.images_shown -= 1
                        self._state.fired = False
                        self._missle.y = -10
                        self._explosions = gallerytarget.getexploded_images()
                        if gallerytarget.nodeduction:
                            self._state.explosion = self._explosions.pop(0)
                            for b in gallerytarget.get_bomb(self._player.x):
                                self._bombs.append(b)
            else:
                if self._state.images_shown < len(self._targets):
                    zz = random.randint(1, 100)
                    if zz < 50:
                        gallerytarget.shown = True
                        self._state.images_shown += 1
                        if gallerytarget.start_x < 0:
                            gallerytarget.start_x = 810
                            gallerytarget.x = 810
                        else:
                            gallerytarget.start_x = -10
                            gallerytarget.x = -10
        if self._state.explosion is not None:
            self._screen.blit(self._state.explosion, (self._saved_x, self._saved_y))

    def player_movement_missle_movement(self):
        """player movement"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self._running = False

        if keys[pygame.K_LEFT] and self._score > -10:
            self._player.move_x_player(-1)
        if keys[pygame.K_RIGHT] and self._score > -10:
            self._player.move_x_player(1)
        if keys[pygame.K_SPACE]:
            if not self._state.fired and self._score > -10 and self._state.explosion is None:
                self._state.shots_fired = 1
                self._fire_sound.play()
                self._missle.x = (
                    self._player.x + self._player.width / 2 - self._missle.width / 2
                )
                self._missle.y = self._player.y - self._missle.height - 1
                self._state.fired = True

        if self._state.fired:
            self.fire_missle()
            pygame.display.update(self._missle.rect)  # Update the display

        if self._missle.y < 0:
            self._state.fired = False
            self._missle.y = 650

        if self._score > -10:
            self._screen.blit(self._player.image, (self._player.x, self._player.y))

    def start(self):
        """Main game loop."""
        self._sound.stop()
        self._clock = pygame.time.Clock()
        self._targets = []
        self._running = True
        self._starting = True
        self.load_resources()
        self._saved_x = 0
        self._saved_y = 0
        self._explosions = []
        self._score = 0
        self._max_score = 0
        self._bombs = []
        self._game_over_images = []
        self._fleas = []
        self._state = State()

        self._clock.tick(60)  # Limit to 60 FPS
        self._screen.fill((0, 0, 0))  # Clear the screen with black
        self.load_enemy()

        self._state.game_over_done = False

        while self._running:
            self.render_score()
            self.player_movement_missle_movement()
            self.load_enemy()
            self.flea_movement()
            self._state.images_shown = 0

            self.game_over()

            self.target_movement()
            self.exploded_target()
            pygame.display.update()

        if self._state.game_over_done:
            self._sound = None
            self.run()

        pygame.display.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
