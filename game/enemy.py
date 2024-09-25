import pygame
import random
from config import *
from utils.asset_loader import load_image

class Enemy:
    def __init__(self):
        self.image = load_image('enemy.png')
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, 30)
        self.speed = ENEMY_SPEED * random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed
        self.rect.y += 1
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed = -self.speed
            # self.rect.y += ENEMY_DROP

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, bullet):
        return self.rect.colliderect(bullet.rect)
