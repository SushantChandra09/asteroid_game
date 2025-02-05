import pyxel

from Asteroid import Asteroid
from settings import *
from Asteroid import *
from math import sin, cos, radians, sqrt


class Bullet:
    def __init__(self, x, y, rotation, color, owner):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.speed = bullet["speed"]
        self.color = color
        self.owner = owner

    def move(self):
        # Move statement
        self.x += self.speed * cos(radians(self.rotation)) * game["frame"]
        self.y += self.speed * sin(radians(self.rotation)) * game["frame"]

    def draw(self):
        # Draw a little rectangle on the screen.
        pyxel.rect(self.x, self.y, 1, 1, self.color)

    def check_limit(self):
        # Delete bullet from the list if it's out of the screen.
        if (self.x < 0 or self.x > game["width"]) or (self.y < 0 or self.y > game["height"]):
            bullet["bullets"].remove(self)

    def verify_collision(self):
        # Verify collision with asteroids
        points = 0
        for a in asteroid["asteroids"]:
            if sqrt((self.x - a.x) ** 2 + (self.y - a.y) ** 2) < a.size:
                points += 1
                if a.size == min(asteroid["radius"]):
                    try:
                        bullet["bullets"].remove(self)
                        asteroid["asteroids"].remove(a)
                    except ValueError:
                        pass
                else:
                    ast = asteroid["asteroids"].pop(asteroid["asteroids"].index(a))
                    asteroid["asteroids"].append(Asteroid(x=ast.x, y=ast.y,
                                                          rotation=ast.rotation + 45,
                                                          size=min(asteroid["radius"]), was_divided=True))
                    asteroid["asteroids"].append(Asteroid(x=ast.x, y=ast.y,
                                                          rotation=ast.rotation - 45,
                                                          size=min(asteroid["radius"]), was_divided=True))
        return points

