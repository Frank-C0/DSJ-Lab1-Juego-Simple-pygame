# game/game.py
import pygame
from pygame import mixer
from config import *
from game.player import Player
from game.enemy import Enemy
from game.bullet import Bullet
from utils.asset_loader import load_image, load_sound

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invader")
        pygame.display.set_icon(load_image('ufo.png'))
        
        self.clock = pygame.time.Clock()
        self.background = load_image('fondo_oscuro2.png')
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.over_font = pygame.font.Font('freesansbold.ttf', 64)
        
        mixer.music.load(load_sound("background.mp3"))
        mixer.music.play(-1)
        
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)
        self.enemies = [Enemy() for _ in range(NUM_ENEMIES)]
        self.bullet = Bullet()
        
        self.score = 0
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            self.player.handle_event(event)
            self.bullet.handle_event(event, self.player)
        return True

    def update(self):
        if not self.game_over:
            self.player.update()
            self.bullet.update()

            for enemy in self.enemies:
                enemy.update()

                # Verificar colisión entre bala y enemigo
                if enemy.check_collision(self.bullet):
                    self.score += 1
                    enemy.reset()
                    self.bullet.reset()

                    explosionSound = mixer.Sound(load_sound("explosion.wav")) 
                    explosionSound.play()

                shrink_factor = 0.5  # Porcentaje para reducir el rectángulo 
                reduced_enemy_rect = enemy.rect.inflate(-enemy.rect.width * (1 - shrink_factor), -enemy.rect.height * (1 - shrink_factor))
                reduced_player_rect = self.player.rect.inflate(-self.player.rect.width * (1 - shrink_factor), -self.player.rect.height * (1 - shrink_factor))

                # Verificar colisión con los rectángulos reducidos
                if reduced_enemy_rect.colliderect(reduced_player_rect):
                    self.game_over = True
                    gameOverSound = mixer.Sound(load_sound("gameover.wav"))
                    gameOverSound.play()
                    
                # Si el enemigo llega al fondo, termina el juego
                if enemy.rect.y > SCREEN_HEIGHT - 160:
                    self.game_over = True

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.bullet.draw(self.screen)
        self.draw_score()
        if self.game_over:
            self.draw_game_over()
        pygame.display.update()

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def draw_game_over(self):
        over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(over_text, (200, 250))

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            self.update()
            self.draw()
