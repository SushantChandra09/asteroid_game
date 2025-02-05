import pyxel
from settings import *
from Bullet import *
from math import sin, cos, radians, sqrt
from random import randint, choice


class Enemy:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.rotation = 0
        self.newrotation = 0
        self.color = enemy["color"]
        self.speed = enemy["speed"]
        self.trisize = enemy["trisize"]
        self.last_shot = game["elapsed_time"]
        self.collision_disabled = False
        self.tricoordinates = {
            "x1": 0, "y1": 0, "x2": 0, "y2": 0, "x3": 0, "y3": 0
        }
        self.spawn()

    def set_location(self):
        # Same logic of asteroids' statement.
        if choice(["H", "V"]) == "V":
            self.x = choice([-self.trisize, game["width"] + self.trisize])
            self.y = randint(-self.trisize, game["height"] + self.trisize)
            if self.x == -self.trisize:
                self.rotation = randint(-79, 79)
            else:
                self.rotation = randint(101, 259)
        elif choice(["H", "V"]) == "H":
            self.x = randint(-self.trisize, game["height"] + self.trisize)
            self.y = choice([-self.trisize, game["width"] + self.trisize])
            if self.y == -self.trisize: self.rotation = randint(10, 169)
            else: self.rotation = randint(191, 349)
        if self.x == 0 and self.y == 0: self.set_location()
        self.newrotation = self.rotation

    def spawn(self):
        # Same logic for asteroids' statement.
        self.set_location()
        if (game["elapsed_time"] - enemy["last_spawn"]) >= enemy["limit_time"]:
            enemy["enemies"].append(self)
            enemy["last_spawn"] = game["elapsed_time"]

    def check_limit(self):
        # If the enemy is out of the screen, delete it from the list.
        if (self.x < -self.trisize or self.x > game["width"] + self.trisize) or (self.y < -self.trisize or self.y > game["height"] + self.trisize):
            enemy["enemies"].remove(self)

    def draw(self):
        # Draw triangle on the screen.
        pyxel.trib(
            self.tricoordinates["x1"], self.tricoordinates["y1"],
            self.tricoordinates["x2"], self.tricoordinates["y2"],
            self.tricoordinates["x3"], self.tricoordinates["y3"],
            self.color)

        pyxel.line(self.tricoordinates["x2"], self.tricoordinates["y2"],
                   self.tricoordinates["x3"], self.tricoordinates["y3"],
                   pyxel.COLOR_BLACK)

    def move(self):
        # Motion logic.
        self.x += self.speed * cos(radians(self.rotation)) * game["frame"]
        self.y += self.speed * sin(radians(self.rotation)) * game["frame"]

        self.tricoordinates["x1"] = self.x + cos(radians(self.newrotation)) * (self.trisize/2) / cos(radians(30))
        self.tricoordinates["y1"] = self.y + sin(radians(self.newrotation)) * (self.trisize/2) / cos(radians(30))
        self.tricoordinates["x2"] = self.x + cos(radians(self.newrotation + 120)) * (self.trisize/2) / cos(radians(30))
        self.tricoordinates["y2"] = self.y + sin(radians(self.newrotation + 120)) * (self.trisize/2) / cos(radians(30))
        self.tricoordinates["x3"] = self.x + cos(radians(self.newrotation + 240)) * (self.trisize/2) / cos(radians(30))
        self.tricoordinates["y3"] = self.y + sin(radians(self.newrotation + 240)) * (self.trisize/2) / cos(radians(30))

        self.bulletx = self.x + cos(radians(self.newrotation)) * ((self.trisize + 1) / 2) / cos(radians(30))
        self.bullety = self.y + sin(radians(self.newrotation)) * ((self.trisize + 1) / 2) / cos(radians(30))

    def shot(self):
        # Shoots if it's in the limit time.
        if (game["elapsed_time"] - self.last_shot) > enemy["bullet_limit_time"]:
            bullet["bullets"].append(Bullet(self.x, self.y, self.newrotation, pyxel.COLOR_RED, self))
            self.last_shot = game["elapsed_time"]

    def verify_collision(self):
        # Check collision with bullets, asteroids and other enemies.
        for b in bullet["bullets"]:
            if (sqrt((b.x - self.x) ** 2 + (b.y - self.y) ** 2) < self.trisize/2) and b.owner != self:
                enemy["enemies"].remove(self)
        for a in asteroid["asteroids"]:
            if sqrt((a.x - self.x) ** 2 + (a.y - self.y) ** 2) < a.size + self.trisize / 2:
                enemy["enemies"].remove(self)

        try:
            other_enemies = enemy["enemies"].copy()
            other_enemies.remove(self)
            for o in other_enemies:
                if sqrt((o.x - self.x) ** 2 + (o.y - self.y) ** 2) < self.trisize:
                    enemy["enemies"].remove(self)
                    enemy["enemies"].remove(o)
                    break
        except ValueError:
            pass



