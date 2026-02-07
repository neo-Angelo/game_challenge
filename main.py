from player import Player
from level import Level
from stats import PlayerStats
from enemy import ChasingEnemy
import random

WIDTH = 800
HEIGHT = 600

level = Level()
player_stats = PlayerStats(max_hp=5)

player = Player(
    pos=(WIDTH // 2, HEIGHT // 2), 
    total_frames=8,
    scale=3,
    speed=200,
    anim_speed=0.1,
    images=images
)

enemies = []
for _ in range(5):
    rand_col = random.randint(2, level.cols - 2)
    rand_row = random.randint(2, level.rows - 2)
    ex = rand_col * 48
    ey = rand_row * 48
    
    random_speed = random.randint(90, 130)
    
    new_enemy = ChasingEnemy(ex, ey, image_prefix="skeleton", speed=random_speed)
    enemies.append(new_enemy)

camera_x = 0
camera_y = 0

def update(dt):
    global camera_x, camera_y
    
    player.update(dt, keyboard, level.width_px, level.height_px)
    
    for enemy in enemies:
        enemy.update(dt, level.width_px, level.height_px, player.actor.pos)
        
        if player.hitbox.colliderect(enemy.hitbox):
            # Verifica se o player JÁ está invencível
            if player.invincible_timer <= 0:
                player_stats.take_damage(1)
                player.start_invincibility(1.5) # Fica piscando por 1.5 segundos
                print("Ai! Dano recebido.")

    current_w = screen.surface.get_width()
    current_h = screen.surface.get_height()
    target_x = player.actor.x - current_w // 2
    target_y = player.actor.y - current_h // 2
    camera_x = target_x
    camera_y = target_y
    max_cam_x = level.width_px - current_w
    max_cam_y = level.height_px - current_h
    camera_x = max(0, min(camera_x, max_cam_x))
    camera_y = max(0, min(camera_y, max_cam_y))

def draw():
    screen.clear()
    level.draw(screen, images, camera_x, camera_y)
    
    for enemy in enemies:
        enemy.draw(screen, camera_x, camera_y)
    
    player.draw(screen, camera_x, camera_y)
    player_stats.draw(screen, images)

