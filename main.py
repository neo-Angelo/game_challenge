from player import Player
from level import Level
from stats import PlayerStats
from enemy import SmartEnemy, WitchEnemy 
import random
import math 
from pgzero.builtins import mouse, keyboard
from sound import SoundManager
from uis import UIManager

WIDTH = 800
HEIGHT = 600


level = Level()
player_stats = PlayerStats(max_hp=5)
sound_manager = SoundManager()
ui = UIManager(sound_manager)


sound_manager.play_menu_music()

start_x = WIDTH // 2
start_y = HEIGHT // 2
camera_x = 0
camera_y = 0
SAFE_RADIUS = 250 

player = Player(
    pos=(start_x, start_y), 
    total_frames=8,
    scale=3,
    speed=200,
    anim_speed=0.08,
    images=images
)

enemies = []

def get_safe_spawn_pos():

    while True:
        rand_col = random.randint(2, level.cols - 2)
        rand_row = random.randint(2, level.rows - 2)
        ex = rand_col * 48
        ey = rand_row * 48
        dx = ex - start_x
        dy = ey - start_y
        dist = math.sqrt(dx**2 + dy**2)
        if dist > SAFE_RADIUS:
            return ex, ey

def reset_game():

    global enemies, camera_x, camera_y
    
    player.actor.pos = (start_x, start_y)
    player_stats.hp = player_stats.max_hp
    player.invincible_timer = 0
    player.state = "idle"
    
    enemies = []

    for _ in range(15): 
        ex, ey = get_safe_spawn_pos()
        speed = random.randint(90, 110)
        enemies.append(SmartEnemy(ex, ey, "skeleton", speed))


    for _ in range(9): 
        ex, ey = get_safe_spawn_pos()
        enemies.append(WitchEnemy(ex, ey, "witch", 140))
        
    camera_x = 0
    camera_y = 0
    

    sound_manager.play_background_music()

def on_mouse_down(pos, button):
    action = ui.handle_click(pos)
    
    if action == "reset_game":
        reset_game() 
        return

    elif action == "goto_menu":
        sound_manager.play_menu_music() 
        return

    if ui.current_state == "game":
        if button == mouse.LEFT:
            player.start_attack()

def update(dt):
    global camera_x, camera_y
    
    if ui.current_state != "game":
        return


    if player_stats.hp <= 0:
        ui.current_state = "game_over"
        sound_manager.play_gameover_music() 
        return


    if len(enemies) == 0:
        ui.current_state = "win"
        sound_manager.play_win_music() 
        return


    player.update(dt, keyboard, level.width_px, level.height_px)
    
    alive_enemies = []
    for enemy in enemies:
        enemy.update(dt, level.width_px, level.height_px, player.actor.pos)
        
        if player.hitbox.colliderect(enemy.hitbox):
            if player.invincible_timer <= 0:
                sound_manager.play_player_damage() 
                player_stats.take_damage(1)
                player.start_invincibility(1.5)
        
        if player.state == "attack1" and not player.has_dealt_damage:
            if player.current_frame >= 3: 
                if player.attack_hitbox.colliderect(enemy.hitbox):
                    sound_manager.play_enemy_damage() 
                    is_dead = enemy.take_damage(1)
                    player.has_dealt_damage = True 
                    if is_dead: continue 

        alive_enemies.append(enemy)
    enemies[:] = alive_enemies


    current_w = screen.surface.get_width()
    current_h = screen.surface.get_height()
    target_x = player.actor.x - current_w // 2
    target_y = player.actor.y - current_h // 2
    max_cam_x = level.width_px - current_w
    max_cam_y = level.height_px - current_h
    camera_x = max(0, min(target_x, max_cam_x))
    camera_y = max(0, min(target_y, max_cam_y))

def draw():
    screen.clear()
    
    if ui.current_state == "menu":
        ui.draw(screen)
    
    elif ui.current_state == "game":
        level.draw(screen, images, camera_x, camera_y)
        for enemy in enemies:
            enemy.draw(screen, camera_x, camera_y)
        player.draw(screen, camera_x, camera_y)
        player_stats.draw(screen, images)
        
    elif ui.current_state in ["game_over", "win"]:
        level.draw(screen, images, camera_x, camera_y)
        for enemy in enemies:
            enemy.draw(screen, camera_x, camera_y)
        player.draw(screen, camera_x, camera_y)
        ui.draw(screen)