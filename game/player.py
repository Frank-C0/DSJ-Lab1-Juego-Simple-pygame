import pygame
from config import *
from utils.asset_loader import load_image
import math

class Player:
    def __init__(self, x, y):
        self.image = load_image('player.png')
        self.image = pygame.transform.rotate(self.image, -90)

        self.original_image = self.image  # Guardamos la imagen original para rotarla
        self.rect = self.image.get_rect(midbottom=(x, y))
        
        # Posición y velocidad como vectores
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        
        # Parámetros de inercia y movimiento
        self.acceleration_factor = 0.2
        self.max_speed = 5
        self.friction = 0.9
        self.min_distance = 20  # Distancia mínima para detenerse cerca del mouse

    def handle_event(self, event):
        # Aquí puedes manejar otros eventos si es necesario
        pass

    def update(self):

        mouse_pos = pygame.mouse.get_pos()
        # Calcular la distancia al mouse
        distance = pygame.Vector2(mouse_pos).distance_to(self.pos)

        # Calcular el ángulo hacia el mouse
        angle = self.calculate_angle(self.pos, mouse_pos)
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.pos)

        # Movimiento con aceleración hacia el mouse
        if distance > self.min_distance:
            direction = (pygame.Vector2(mouse_pos) - self.pos).normalize()
            acceleration = direction * self.acceleration_factor
            self.velocity += acceleration
        else:
            self.velocity *= self.friction

        # Limitar la velocidad máxima
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        velocity = self.velocity * 0.90

        # Actualizar la posición del jugador con la velocidad
        self.pos += self.velocity
        self.rect.center = self.pos

        # clamp position to screen and reset velocity
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.rect.left == 0 or self.rect.right == SCREEN_WIDTH:
            self.velocity.x = 0
        if self.rect.top == 0 or self.rect.bottom == SCREEN_HEIGHT:
            self.velocity.y = 0
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def calculate_angle(self, from_pos, to_pos):
        # Calcula el ángulo en grados entre dos puntos
        dx, dy = to_pos[0] - from_pos[0], to_pos[1] - from_pos[1]
        return math.degrees(math.atan2(-dy, dx))
