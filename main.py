import sys
import os
import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 600, 300
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space War")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Jugador
players_folder = 'assets/players'
player_files = os.listdir(players_folder)
player_images = [pygame.image.load(os.path.join(players_folder, filename)) for filename in player_files]
player_images = [pygame.transform.scale(player_image, (50, 50)) for player_image in player_images]
player_rect = player_images[0].get_rect(centerx=WIDTH // 2, bottom=HEIGHT - 20)
PLAYER_SPEED = 5

# Enemigos
meteors_folder = 'assets/enemies/meteors'
planets_folder = 'assets/enemies/planets'
meteors_files = os.listdir(meteors_folder)
planets_files = os.listdir(planets_folder)
meteors_images = [pygame.image.load(os.path.join(meteors_folder, filename)) for filename in meteors_files]
planets_images = [pygame.image.load(os.path.join(planets_folder, filename)) for filename in planets_files]
enemy_images = [pygame.transform.scale(img, (50, 50)) for img in meteors_images + planets_images]


def draw_window(player_rect, enemies):
    """Dibuja los elementos en la pantalla.

        Args:
            player_rect (pygame.Rect): Rectángulo que representa al jugador.
            enemies (list): Lista de tuplas que contiene los rectángulos de los enemigos y sus índices de imagen.
    """
    WIN.fill(BLACK)
    WIN.blit(player_images[player_index], player_rect)
    for enemy, _ in enemies:
        WIN.blit(enemy_images[enemy_index], enemy)
    pygame.display.update()

def main():
    """Función principal del juego."""
    global enemy_index, ENEMY_SPEED
    ENEMY_SPEED = 5
    run = True

    while run:
        clock = pygame.time.Clock()
        player_alive = True
        score = 0
        enemies = []
        SPAWN_RATE = 50

        while player_alive:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_rect.left > 0:
                player_rect.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
                player_rect.x += PLAYER_SPEED

            updated_enemies = []

            for enemy, enemy_index in enemies:
                enemy.y += ENEMY_SPEED
                if enemy.bottom < HEIGHT:
                    updated_enemies.append((enemy, enemy_index))
                else:
                    score += 1

            enemies = updated_enemies

            if random.randrange(SPAWN_RATE) == 0:
                enemy_index = random.randint(0, len(enemy_images) - 1)
                enemy_rect = enemy_images[enemy_index].get_rect(x=random.randrange(WIDTH - 50), y=-50)
                enemies.append((enemy_rect, enemy_index))

            for enemy, _ in enemies:
                if player_rect.colliderect(enemy):
                    player_alive = False

            draw_window(player_rect, enemies)

        font = pygame.font.SysFont(None, 24)
        game_over_text = font.render(f"Tu nave ha colisionado. Superaste {score} objetos espaciales.", True, WHITE)
        game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - game_over_text.get_height()))

        retry_text = font.render("Presiona otra tecla para reintentarlo o ESC para salir.", True, RED)
        retry_text_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + game_over_text.get_height()))

        WIN.blit(game_over_text, game_over_text_rect)
        WIN.blit(retry_text, retry_text_rect)
        pygame.display.update()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    waiting_for_input = False


def player_selection_menu():
    """Muestra el menú de selección de jugador."""
    global player_index
    player_index = 0
    run = True

    while run:
        WIN.fill(BLACK)
        font = pygame.font.SysFont(None, 30)
        title = font.render("Pilot A452, selecciona tu nave", True, WHITE)
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        MARGIN = 10
        LEFT_MARGIN = 30

        for idx, player_image in enumerate(player_images):
            rect = player_image.get_rect(centerx=(WIDTH // 2) - ((len(player_images) * 50 + (len(player_images) - 1) * MARGIN) // 2) + (idx * (50 + MARGIN)) + LEFT_MARGIN, centery=HEIGHT // 2)
            rect.centerx += MARGIN // 2
            WIN.blit(player_image, rect)
            if idx == player_index:
                pygame.draw.rect(WIN, WHITE, rect, 2)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_index = (player_index - 1) % len(player_images)
                elif event.key == pygame.K_RIGHT:
                    player_index = (player_index + 1) % len(player_images)
                elif event.key == pygame.K_RETURN:
                    run = False

    main()


if __name__ == "__main__":
    player_selection_menu()
