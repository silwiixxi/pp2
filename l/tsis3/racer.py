import pygame
import random

WIDTH, HEIGHT = 400, 600
LANES = [80, 180, 280]

class Player:
    def __init__(self):
        self.lane = 1
        self.y = 500
        self.speed = 5
        self.power = None
        self.power_timer = 0

    def move(self, direction):
        self.lane = max(0, min(2, self.lane + direction))

    def update(self):
        if self.power == "nitro":
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power = None

    def get_x(self):
        return LANES[self.lane]


class Enemy:
    def __init__(self):
        self.lane = random.randint(0, 2)
        self.y = -100

    def update(self, speed):
        self.y += speed


class PowerUp:
    TYPES = ["nitro", "shield", "repair"]

    def __init__(self):
        self.lane = random.randint(0, 2)
        self.type = random.choice(self.TYPES)
        self.y = -100

    def update(self, speed):
        self.y += speed