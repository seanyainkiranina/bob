""" " Module for defining the Target class used in the game."""

import os
import random
import pygame
from pygame.locals import (  # pylint: disable=[E0611,W0611]
    QUIT,  # pylint: disable=[E0611,W0611]
    KEYDOWN,  # pylint: disable=[E0611,W0611]
    K_UP,  # pylint: disable=[E0611,W0611]
    K_DOWN,  # pylint: disable=[E0611,W0611]
    K_LEFT,  # pylint: disable=[E0611,W0611]
    K_RIGHT,  # pylint: disable=[E0611,W0611]
)  # pylint: disable=[E0611,W0611]


class Target:
    """Represents a target in the game with a name and visibility status."""

    def __init__(self, name, x=0, y=0, maxX=810, minX=-10, maxY=600, minY=-10):
        self._name = name
        self._shown = False
        self._x = x
        self._y = y
        self._main_dir = os.path.split(os.path.abspath(__file__))[0]
        self._data_dir = os.path.join(self._main_dir, "..\\images")
        self._image = self.getimage()
        self._image_left = self.image
        self._image_right = self.getrightimage()
        self._rect = self._image.get_rect()
        self._max_x = maxX
        self._min_x = minX
        self._max_y = maxY
        self._min_y = minY
        self._start_x = x
        self._bullets = []

    @property
    def rect(self):
        """Returns the rect."""
        return self._rect

    @property
    def image(self):
        """Returns the image of the target."""
        return self._image

    @property
    def height(self):
        """Returns the height of the image."""
        return self._image.get_height()

    @property
    def width(self):
        """Returns the width of the image."""
        return self._image.get_width()

    @property
    def name(self):
        """Returns the name of the target."""
        return self._name

    @property
    def shown(self):
        """Returns whether the target is shown."""
        return self._shown

    @shown.setter
    def shown(self, value):
        """Sets the visibility of the target."""
        self._shown = value

    @property
    def start_x(self):
        """Returns the starting X coordinate of the target."""
        return self._start_x

    @start_x.setter
    def start_x(self, value):
        """Returns the starting X coordinate of the target."""
        self._start_x = value

    @property
    def x(self):
        """Returns the X coordinate of the target."""
        return self._x

    @x.setter
    def x(self, value):
        """Sets the X coordinate of the target."""
        self._x = value

    @property
    def y(self):
        """Returns the Y coordinate of the target."""
        return self._y

    @y.setter
    def y(self, value):
        """Sets the Y coordinate of the target."""
        self._y = value

    def explode(self):
        """Handles the explosion of the target."""
        self._shown = False
        return self.start_x

    def get_bomb(self, x):
        """Get a bullet"""
        bombs = self.get_bullets(x)
        b = []
        total_bombs = random.randint(1, 5)
        lb = 0
        while lb < total_bombs:
            which_bomb = random.randint(0, len(bombs) - 1)
            bomb = bombs[which_bomb]
            bomb.x = bomb.x + random.randint(-2, 4)
            bomb.y = bomb.y + random.randint(-4, 4)
            b.append(bombs[which_bomb])
            lb += 1

        return b

    def get_bullets(self, x):
        """Returns the list of bullets."""
        for b in range(0, 6):
            self._bullets.append(Target(f"bullet{b}", x, self._y))
        return self._bullets

    def get_game_over_images(self):
        """Returns the explosion image for the target."""
        exploded_images = []
        for i in range(0, 18):
            explosion_path = os.path.join(self._data_dir, f"explosion{i}.png")
            if os.path.exists(explosion_path):
                exploded_images.append(pygame.image.load(explosion_path))
            else:
                raise FileNotFoundError(
                    f"Explosion image for target '{self._name}' not found at {explosion_path}"
                )
        return exploded_images

    def getexploded_images(self):
        """Returns a list of exploded images for the target."""
        exploded_images = []
        for i in range(0, 5):
            image_path = os.path.join(self._data_dir, f"enemy_boom{i}.png")
            if os.path.exists(image_path):
                exploded_images.append(pygame.image.load(image_path))
            else:
                raise FileNotFoundError(
                    f"Exploded image for target '{self._name}' not found at {image_path}"
                )
        return exploded_images

    def getimage(self):
        """Returns the image of the target based on its name."""
        image_path = os.path.join(self._data_dir, f"{self._name}.png")
        if os.path.exists(image_path):
            return pygame.image.load(image_path)
        else:
            raise FileNotFoundError(
                f"Image for target '{self._name}' not found at {image_path}"
            )

    def getrightimage(self):
        """Returns the image of the target based on its name."""
        image_path = os.path.join(self._data_dir, f"{self._name}_right.png")
        if os.path.exists(image_path):
            return pygame.image.load(image_path)
        else:
            raise FileNotFoundError(
                f"Image for target '{self._name}' not found at {image_path}"
            )

    def move_x_player(self, delta):
        """Moves the target in the X direction by delta, ensuring it stays within bounds."""
        new_x = self._x + delta
        if new_x < self._min_x:
            new_x = self._min_x
        if new_x > self._max_x:
            new_x = self._max_x
        self._x = new_x

    def move_x_target(self, delta):
        """Moves the target in the X direction by delta, ensuring it stays within bounds."""
        result = 0
        if self._start_x > 0:
            delta = -delta
        else:
            delta = abs(delta)

        last_x = self._x
      
        new_x = self._x + delta
        if new_x < self._min_x:
            new_x = self._start_x
            result = -2
        if new_x > self._max_x:
            new_x = self._start_x
            result = -2
        self._x = new_x

        if self._x != last_x:
            if self._x > last_x:
                self._image = self._image_left
            else:
                self._image = self._image_right

        return result

    def move_up(self):
        """Moves the target in the Y direction by delta, ensuring it stays within bounds."""
        new_y = self._y - 2
        if new_y < self._min_y:
            new_y = self._min_y
        if new_y >= self._max_y:
            new_y = self._min_y
        self._y = new_y

    def move_down(self):
        """Moves the target in the Y direction by delta, ensuring it stays within bounds."""
        new_y = self._y - 1
        if new_y < self._min_y:
            new_y = self._max_y
        self._y = new_y
