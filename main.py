from player import Player
from level import Level
from stats import PlayerStats
from enemy import RoamingEnemy, ChasingEnemy
import random

# Necessário para detectar botões do mouse
from pgzero.builtins import mouse 

WIDTH = 800
HEIGHT = 600

level = Level()
player_stats = PlayerStats(max_hp=5)

player = Player(
    pos=(WIDTH // 2, HEIGHT // 2), 
    total_frames=8,
    scale=3,
    speed=200,
    anim_speed=0.08, # Um pouco mais rápido para a animação fluir bem
    images=images
)

enemies = []
# Criação de inimigos (mantida igual)
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

# --- NOVO: INPUT DO MOUSE ---
def on_mouse_down(pos, button):
    if button == mouse.LEFT:
        player.start_attack()

def update(dt):
    global camera_x, camera_y
    
    player.update(dt, keyboard, level.width_px, level.height_px)
    
    # Lista de inimigos vivos para o próximo frame
    alive_enemies = []
    
    for enemy in enemies:
        enemy.update(dt, level.width_px, level.height_px, player.actor.pos)
        
        # 1. Player apanha do Inimigo
        if player.hitbox.colliderect(enemy.hitbox):
            if player.invincible_timer <= 0:
                player_stats.take_damage(1)
                player.start_invincibility(1.5)
        
        # 2. Player ATACA Inimigo
        # Verifica se está atacando e se hitbox azul toca na hitbox vermelha do inimigo
        if player.state == "attack1" and not player.has_dealt_damage:
            # DICA: Só dá dano no meio da animação (ex: frame 3 ou 4 de 0-7)
            # para parecer que bateu na hora que esticou o braço
            if player.current_frame >= 3: 
                if player.attack_hitbox.colliderect(enemy.hitbox):
                    print("Toma essa, esqueleto!")
                    is_dead = enemy.take_damage(1)
                    player.has_dealt_damage = True # Garante apenas 1 hit por clique
                    
                    if is_dead:
                        print("Inimigo derrotado!")
                        continue # Não adiciona na lista alive_enemies, efetivamente removendo-o

        alive_enemies.append(enemy)

    # Atualiza a lista principal removendo os mortos
    enemies[:] = alive_enemies

    # Câmera (mantido)
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
