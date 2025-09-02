import pygame
import sys
import random
import os

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pew Pew Game")

enemy = pygame.image.load("ducky.png").convert_alpha()
enemy = pygame.transform.scale(enemy, (100, 100))
enemy_rect = enemy.get_rect(width=100, height=100)
enemy_speed = 2
enemies = []
enemy_timer = 0
enemy_spawn_time = 2000
clock = pygame.time.Clock()

character_image = pygame.image.load("pewpew.png").convert_alpha()
character_image = pygame.transform.scale(character_image, (50, 50))
character_rect = character_image.get_rect(width=50, height=50)
player_x = screen_width // 2 - character_rect.width // 2
player_y = screen_height - character_rect.height - 10
player_speed = 5

bullet_width = 8
bullet_height = 18
bullet_speed = 7
bullets = []

score = 0
lives = 3
heart_font = pygame.font.SysFont(None, 40)
game_over_font = pygame.font.SysFont(None, 72)
font = pygame.font.SysFont(None, 36)

MAX_AMMO = 10
ammo = MAX_AMMO
reloading = False

HIGHSCORE_FILE = "highscore.txt"
if os.path.exists(HIGHSCORE_FILE):
    with open(HIGHSCORE_FILE, "r") as f:
        try:
            highscore = int(f.read())
        except:
            highscore = 0
else:
    highscore = 0

def save_highscore(new_score):
    global highscore
    if new_score > highscore:
        highscore = new_score
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(highscore))

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def draw_hearts(surface, lives):
    heart_text = "♥ " * lives
    text = heart_font.render(heart_text, True, (255, 0, 0))
    surface.blit(text, (10, 50))

def draw_water_bullet(surface, rect):
    for i in range(rect.height):
        color = (0, 100 + int(155 * (i / rect.height)), 255)
        pygame.draw.rect(surface, color, (rect.x, rect.y + i, rect.width, 1))

def draw_ammo_bar(surface, ammo, max_ammo):
    bar_x = 10
    bar_y = screen_height - 40
    bar_width = 200
    bar_height = 20
    pygame.draw.rect(surface, (255,255,255), (bar_x, bar_y, bar_width, bar_height), 2)
    fill_width = int(bar_width * (ammo / max_ammo))
    pygame.draw.rect(surface, (0, 150, 255), (bar_x, bar_y, fill_width, bar_height))
    ammo_text = font.render(f"Ammo: {ammo}/{max_ammo}", True, (255,255,255))
    surface.blit(ammo_text, (bar_x + bar_width + 10, bar_y - 2))

def show_game_over(surface, score, highscore):
    surface.fill((20, 20, 40))
    pygame.draw.rect(surface, (0, 120, 255), (100, 120, screen_width-200, screen_height-240), 8)
    text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    score_text = heart_font.render(f"Score: {score}", True, (255, 255, 255))
    highscore_text = heart_font.render(f"Highscore: {highscore}", True, (0, 255, 255))
    prompt = font.render("Press ENTER to restart or ESC to quit", True, (200, 200, 200))
    surface.blit(text, (screen_width // 2 - text.get_width() // 2, 180))
    surface.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 280))
    surface.blit(highscore_text, (screen_width // 2 - highscore_text.get_width() // 2, 330))
    surface.blit(prompt, (screen_width // 2 - prompt.get_width() // 2, 400))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(60)

def show_start_screen(surface, highscore):
    surface.fill((20, 20, 40))
    title = game_over_font.render("PEW PEW GAME", True, (0, 200, 255))
    prompt = font.render("Press SPACE to Start", True, (255, 255, 255))
    hs = font.render(f"Highscore: {highscore}", True, (0, 255, 255))
    surface.blit(title, (screen_width // 2 - title.get_width() // 2, screen_height // 2 - 100))
    surface.blit(prompt, (screen_width // 2 - prompt.get_width() // 2, screen_height // 2 + 20))
    surface.blit(hs, (screen_width // 2 - hs.get_width() // 2, screen_height // 2 + 60))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
        clock.tick(60)

def show_instruction_panel(surface):
    surface.fill((30, 30, 60))
    pygame.draw.rect(surface, (0, 120, 255), (80, 160, screen_width-160, screen_height-320), 6)
    title = game_over_font.render("HOW TO PLAY", True, (0, 200, 255))
    controls1 = font.render("Move: LEFT/RIGHT arrows", True, (255, 255, 255))
    controls2 = font.render("Shoot: UP arrow (release to fire)", True, (255, 255, 255))
    controls3 = font.render("Reload: SPACE (any time)", True, (255, 255, 255))
    info = font.render("Shoot ducks, don't let them reach the bottom!", True, (255, 255, 0))
    surface.blit(title, (screen_width // 2 - title.get_width() // 2, 200))
    surface.blit(controls1, (screen_width // 2 - controls1.get_width() // 2, 280))
    surface.blit(controls2, (screen_width // 2 - controls2.get_width() // 2, 320))
    surface.blit(controls3, (screen_width // 2 - controls3.get_width() // 2, 360))
    surface.blit(info, (screen_width // 2 - info.get_width() // 2, 420))
    pygame.display.flip()
    pygame.time.wait(5000)

def reset_game():
    global enemies, bullets, score, lives, enemy_timer, ammo, reloading, enemy_speed, enemy_spawned_count
    enemies = []
    bullets = []
    score = 0
    lives = 3
    enemy_timer = pygame.time.get_ticks()
    ammo = MAX_AMMO
    reloading = False
    enemy_speed = 2
    enemy_spawned_count = 0

show_start_screen(screen, highscore)
show_instruction_panel(screen)
reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_highscore(score)
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and not reloading and ammo > 0:
                bullet_x = player_x + character_rect.width - bullet_width - 2
                bullet_y = player_y + 8
                bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))
                ammo -= 1
                if ammo == 0:
                    reloading = True
            if event.key == pygame.K_SPACE:
                ammo = MAX_AMMO
                reloading = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - character_rect.width:
        player_x += player_speed

    for bullet in bullets:
        bullet.y -= bullet_speed
    bullets[:] = [bullet for bullet in bullets if bullet.y > 0]

    current_time = pygame.time.get_ticks()
    if current_time - enemy_timer > enemy_spawn_time:
        enemy_x = random.randint(0, screen_width - enemy_rect.width)
        enemy_y = -enemy_rect.height
        enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_rect.width, enemy_rect.height))
        enemy_timer = current_time
        enemy_spawned_count += 1
        if enemy_spawned_count % 10 == 0:
            enemy_speed += 0.2  # Increase speed every 10 enemies

    enemies_to_remove = []
    bullets_to_remove = []
    for enemy_rect in enemies:
        enemy_rect.y += enemy_speed
        if enemy_rect.y >= screen_height:
            if enemy_rect not in enemies_to_remove:
                enemies_to_remove.append(enemy_rect)
            lives -= 1
            if lives == 0:
                save_highscore(score)
                show_game_over(screen, score, highscore)
                show_start_screen(screen, highscore)
                show_instruction_panel(screen)
                reset_game()
                break

    for enemy_rect in enemies:
        for bullet in bullets:
            if check_collision(bullet, enemy_rect):
                if enemy_rect not in enemies_to_remove:
                    enemies_to_remove.append(enemy_rect)
                if bullet not in bullets_to_remove:
                    bullets_to_remove.append(bullet)
                score += 1

    enemies = [e for e in enemies if e not in enemies_to_remove]
    bullets = [b for b in bullets if b not in bullets_to_remove]

    screen.fill((0, 0, 0))
    character_rect.topleft = (player_x, player_y)
    screen.blit(character_image, character_rect)
    for bullet in bullets:
        draw_water_bullet(screen, bullet)
    for enemy_rect in enemies:
        screen.blit(enemy, enemy_rect)

    score_text = font.render(f"Score: {score}", True, (255, 255, 0))
    screen.blit(score_text, (screen_width - 180, 10))
    hs_text = font.render(f"Highscore: {highscore}", True, (0, 255, 255))
    screen.blit(hs_text, (screen_width - 180, 40))
    draw_hearts(screen, lives)
    draw_ammo_bar(screen, ammo, MAX_AMMO)
    if reloading:
        reload_text = font.render("Press SPACE to reload!", True, (255, 100, 100))
        screen.blit(reload_text, (20, screen_height - 70))

    pygame.display.flip()
    clock.tick(60)