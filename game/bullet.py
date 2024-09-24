import pygame
from pygame import mixer
from config import *
from utils.asset_loader import load_image, load_sound
import math

class Bullet:
    def __init__(self):
        self.image = load_image('bullet.png')
        # rotar la imagen de la bala hacia la derecha
        self.image = pygame.transform.rotate(self.image, -90)
        self.original_image = self.image  # Guardamos la imagen original para rotarla
        self.rect = self.image.get_rect()
        self.speed = BULLET_SPEED
        self.state = "ready"
        self.direction = pygame.Vector2(0, 0)  # Vector de dirección inicial

    def handle_event(self, event, player):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.state == "ready":
            self.state = "fire"

            self.direction = pygame.Vector2(mouse_pos) - pygame.Vector2(player.rect.center)
            if self.direction.length() > 0:  # Normalizar si la longitud es mayor a 0
                self.direction = self.direction.normalize()

            offset = self.direction * (player.rect.height // 2) 
            self.rect.center = player.rect.center + offset 

            # Rotar la imagen de la bala hacia la dirección del disparo
            angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)

            # Sonido de disparo
            bulletSound = mixer.Sound(load_sound("laser.wav"))
            bulletSound.play()

    def update(self):
        if self.state == "fire":
            self.rect.x += self.direction.x * self.speed
            self.rect.y += self.direction.y * self.speed

            if (self.rect.bottom <= 0 or self.rect.top >= SCREEN_HEIGHT or
                    self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH):
                self.reset()

    def reset(self):
        self.state = "ready"
        self.rect.y = SCREEN_HEIGHT

    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self.image, self.rect)
