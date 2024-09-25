import pygame
import random
from config import *
from utils.asset_loader import load_image
import math

class Rock:
    def __init__(self, player):
        self.image = load_image('rock.png')
        # transform to 1/2 size
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))

        self.rect = self.image.get_rect()
        self.speed = 2

        # Posición inicial aleatoria desde los bordes de la pantalla
        self.spawn_around_screen()

        # Calcular la dirección inicial hacia el jugador
        self.set_direction_towards_player(player)

    def spawn_around_screen(self):
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            self.rect.x = random.randint(0, SCREEN_WIDTH)
            self.rect.y = -self.rect.height
        elif edge == 'bottom':
            self.rect.x = random.randint(0, SCREEN_WIDTH)
            self.rect.y = SCREEN_HEIGHT
        elif edge == 'left':
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, SCREEN_HEIGHT)
        elif edge == 'right':
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(0, SCREEN_HEIGHT)

    def set_direction_towards_player(self, player):
        self.direction = pygame.Vector2(player.rect.center) - pygame.Vector2(self.rect.center)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

    def update(self, player):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Si la roca sale de la pantalla, reaparece en un borde aleatorio
        if (self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0 or
                self.rect.left > SCREEN_WIDTH or self.rect.right < 0):
            self.spawn_around_screen()
            self.set_direction_towards_player(player)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, player):
        
        shrink_factor = 0.5  # Porcentaje para reducir el rectángulo 
        reduced_rock_rect = self.rect.inflate(-self.rect.width * (1 - shrink_factor), -self.rect.height * (1 - shrink_factor))
        reduced_player_rect = player.rect.inflate(-player.rect.width * (1 - shrink_factor), -player.rect.height * (1 - shrink_factor))

        return reduced_rock_rect.colliderect(reduced_player_rect)