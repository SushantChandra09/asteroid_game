import pyxel
from settings import *
from math import sin, cos, radians, sqrt
from random import randint, choice


class Asteroid:
    def __init__(self, x=0, y=0, rotation=0, size=0, was_divided=False):
        self.x = x
        self.y = y
        self.speed = asteroid["speed"]
        self.rotation = rotation
        self.size = size
        self.was_divided = was_divided
        self.spawn()

    # Choose randomly a place for asteroid spawning
    def set_location(self):
        if not self.was_divided:
            self.size = choice(asteroid["radius"])
            if choice(["H", "V"]) == "V":
                # If the asteroid appears vertically, it'll select the superior or inferior margin to come out.
                self.x = choice([-self.size, game["width"] + self.size])
                self.y = randint(-self.size, game["height"] + self.size)
                if self.x == -self.size:
                    self.rotation = randint(-79, 79)
                else:
                    self.rotation = randint(101, 259)
            elif choice(["H", "V"]) == "H":
                # If the asteroid appears horizontally, it'll select the left or right margin to come out.
                self.x = randint(-self.size, game["height"] + self.size)
                self.y = choice([-self.size, game["width"] + self.size])
                if self.y == -self.size:
                    self.rotation = randint(10, 169)
                else:
                    self.rotation = randint(191, 349)
        if self.x == 0 and self.y == 0: self.set_location()

    def spawn(self):
        # Set the location and check if it's in the limit time for spawning.
        self.set_location()
        if (game["elapsed_time"] - asteroid["last_spawn"]) >= asteroid["limit_time"]:
            asteroid["asteroids"].append(self)
            asteroid["last_spawn"] = game["elapsed_time"]

    def move(self):
        # Move statement
        self.x += self.speed * cos(radians(self.rotation)) * game["frame"]
        self.y += self.speed * sin(radians(self.rotation)) * game["frame"]

    def draw(self):
        # Draw a circle
        pyxel.circ(self.x, self.y, self.size, pyxel.COLOR_WHITE)

    def check_limit(self):
        # Delete asteroid from the list if it's out of the screen.
        if (self.x < -self.size or self.x > game["width"] + self.size) or (self.y < -self.size or self.y > game["height"] + self.size):
            asteroid["asteroids"].remove(self)

