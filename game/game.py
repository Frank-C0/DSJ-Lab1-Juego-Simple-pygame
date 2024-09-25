# game/game.py
import pygame
from pygame import mixer
from config import *
from game.player import Player
from game.enemy import Enemy
from game.bullet import Bullet
from game.rock import Rock  # Importar la clase Rock
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
        
        # Inicializar jugador, enemigos, balas y rocas
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)
        self.enemies = [Enemy() for _ in range(NUM_ENEMIES)]
        self.bullet = Bullet()
        self.rocks = [Rock(self.player) for _ in range(2)]
        
        self.score = 0
        self.game_over = False
        self.in_menu = True  # Indica si estamos en el menú de inicio

    def reset(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)
        self.enemies = [Enemy() for _ in range(NUM_ENEMIES)]
        self.bullet = Bullet()
        self.rocks = [Rock(self.player) for _ in range(2)]
        self.score = 0
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Si estamos en el menú y se presiona una tecla, comenzamos el juego
            if self.in_menu:
                if event.type == pygame.KEYDOWN:
                    self.in_menu = False
            elif self.game_over:
                # Si estamos en "game over" y se presiona una tecla, reinicia el juego
                if event.type == pygame.KEYDOWN:
                    self.reset()
            else:
                self.player.handle_event(event)
                self.bullet.handle_event(event, self.player)
        return True

    def update(self):
        if not self.game_over and not self.in_menu:
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
                if enemy.rect.y > SCREEN_HEIGHT - 20:
                    self.game_over = True

            # Actualizar rocas
            for rock in self.rocks:
                rock.update(self.player)

                # Verificar colisión entre el jugador y la roca
                if rock.check_collision(self.player):
                    self.game_over = True
                    gameOverSound = mixer.Sound(load_sound("gameover.wav"))
                    gameOverSound.play()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        if self.in_menu:
            self.draw_menu()
        elif self.game_over:
            self.draw_game_over()
        else:
            pygame.draw.line(self.screen, (255, 0, 0), (0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, SCREEN_HEIGHT - 20), 4)

            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            for rock in self.rocks:
                rock.draw(self.screen)
            self.bullet.draw(self.screen)
            self.draw_score()

        pygame.display.update()

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def draw_game_over(self):
        over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(over_text, (200, 250))
        retry_text = self.font.render("Presiona cualquier tecla para reiniciar", True, (255, 255, 255))
        self.screen.blit(retry_text, (150, 350))

    def draw_menu(self):
        menu_text = self.over_font.render("SPACE INVADER", True, (255, 255, 255))
        self.screen.blit(menu_text, (150, 200))
        
        start_text = self.font.render("Presiona cualquier tecla para jugar", True, (20, 255, 255))
        start_text2 = self.font.render("Elimina a los enemigos,", True, (10, 200, 70))
        start_text3 = self.font.render("esquiva los asteroides", True, (10, 200, 70))
        
        self.screen.blit(start_text, (160, 300))
        self.screen.blit(start_text2, (160, 350))
        self.screen.blit(start_text3, (160, 400))


    def run(self):
        """Ciclo principal del juego"""
        running = True
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            self.update()
            self.draw()
