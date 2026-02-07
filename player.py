from pgzero.actor import Actor
from pygame import Rect
import math

TILE_SIZE = 48 

class Player:
    def __init__(self, pos, total_frames, scale, speed, anim_speed, images):
        self.images = images
        self.total_frames = total_frames 
        self.scale = scale 
        self.speed = speed 
        self.anim_speed = anim_speed
        
        # --- NOVO: Velocidade específica para o ataque ---
        # Quanto menor o número, mais rápida a animação.
        # Se anim_speed normal é 0.08 ou 0.1, 0.05 será bem rapidinho.
        self.attack_anim_speed = 0.05 

        self.state = "idle"
        self.direction = "down"

        self.current_frame = 0
        self.frame_timer = 0

        self.actor = Actor("idle_down_0", pos=pos)
        
        self.target_x = self.actor.x
        self.target_y = self.actor.y
        self.is_moving = False

        # Hitbox de corpo
        hitbox_size = 30
        self.hitbox = Rect(0, 0, hitbox_size, hitbox_size)
        
        # Hitbox de Ataque
        self.attack_hitbox = Rect(0, 0, 0, 0)
        self.is_attacking = False
        self.has_dealt_damage = False 

        self.animations = self._load_animations()
        self.actor._surf = self.animations["idle_down"][0]
        self._sync_hitbox()
        
        self.invincible_timer = 0

    def _load_animation(self, base_name):
        frames = []
        for i in range(self.total_frames):
            try:
                img = getattr(self.images, f"{base_name}_{i}")
                frames.append(img)
            except AttributeError:
                pass 
        return frames

    def _load_animations(self):
        anims = {}
        for state in ["idle", "run", "attack1"]:
            for direction in ["up", "down", "left", "right"]:
                key = f"{state}_{direction}"
                anims[key] = self._load_animation(key)
        return anims

    def update(self, dt, keyboard, map_width, map_height):
        if self.invincible_timer > 0:
            self.invincible_timer -= dt

        if self.state == "attack1":
            self._update_attack_hitbox()
            self._animate(dt)
            return 

        if self.is_moving:
            self._continue_moving(dt)
            self._animate(dt)
        else:
            self._check_input(keyboard, map_width, map_height)
            self._animate(dt)
            
        self._sync_hitbox()

    def start_attack(self):
        if not self.is_moving and self.state != "attack1":
            self.state = "attack1"
            self.current_frame = 0
            self.frame_timer = 0
            self.has_dealt_damage = False 

    def _update_attack_hitbox(self):
        """Gera um retângulo na frente do player"""
        # --- MUDANÇA AQUI: Aumentando o tamanho da hitbox azul ---
        # Antes era 40. Aumentei para 70 (ficou bem grande e fácil de acertar)
        atk_size = 70   
        
        # Aumentei um pouco o offset (distância do centro) de 40 para 50
        # para o quadrado maior não ficar muito em cima do player.
        offset_dist = 50 
        
        center_x, center_y = self.actor.pos
        
        if self.direction == "left":
            self.attack_hitbox = Rect(center_x - offset_dist - atk_size/2, center_y - atk_size/2, atk_size, atk_size)
        elif self.direction == "right":
            self.attack_hitbox = Rect(center_x + offset_dist - atk_size/2, center_y - atk_size/2, atk_size, atk_size)
        elif self.direction == "up":
            self.attack_hitbox = Rect(center_x - atk_size/2, center_y - offset_dist - atk_size/2, atk_size, atk_size)
        elif self.direction == "down":
            self.attack_hitbox = Rect(center_x - atk_size/2, center_y + offset_dist - atk_size/2, atk_size, atk_size)

    def start_invincibility(self, duration=1.0):
        self.invincible_timer = duration

    def _check_input(self, keyboard, map_width, map_height):
        dx = 0
        dy = 0
        moved = False

        if keyboard.a:
            dx = -TILE_SIZE
            self.direction = "left"
            moved = True
        elif keyboard.d:
            dx = TILE_SIZE
            self.direction = "right"
            moved = True
        elif keyboard.w:
            dy = -TILE_SIZE
            self.direction = "up"
            moved = True
        elif keyboard.s:
            dy = TILE_SIZE
            self.direction = "down"
            moved = True

        if moved:
            next_x = self.actor.x + dx
            next_y = self.actor.y + dy
            margin = TILE_SIZE / 2
            if (margin <= next_x <= map_width - margin) and \
               (margin <= next_y <= map_height - margin):
                self.target_x = next_x
                self.target_y = next_y
                self.is_moving = True
                self.state = "run"
            else:
                self.state = "idle"
        else:
            self.state = "idle"

    def _continue_moving(self, dt):
        step = self.speed * dt
        diff_x = self.target_x - self.actor.x
        diff_y = self.target_y - self.actor.y
        dist = math.sqrt(diff_x**2 + diff_y**2)

        if dist <= step:
            self.actor.x = self.target_x
            self.actor.y = self.target_y
            self.is_moving = False 
        else:
            self.actor.x += (diff_x / dist) * step
            self.actor.y += (diff_y / dist) * step

    def _animate(self, dt):
        self.frame_timer += dt
        
        # --- MUDANÇA AQUI: Define qual velocidade usar ---
        # Se estiver atacando, usa a velocidade rápida. Se não, usa a normal.
        current_speed_limit = self.anim_speed
        if self.state == "attack1":
            current_speed_limit = self.attack_anim_speed

        # Usa o limite escolhido acima
        if self.frame_timer < current_speed_limit:
            return

        self.frame_timer = 0
        self.current_frame += 1

        if self.current_frame >= self.total_frames:
            if self.state == "attack1":
                self.state = "idle"
                self.current_frame = 0
                self.attack_hitbox = Rect(0,0,0,0) 
            else:
                self.current_frame = 0

        key = f"{self.state}_{self.direction}"
        if key in self.animations and len(self.animations[key]) > 0:
            idx = self.current_frame % len(self.animations[key])
            self.actor._surf = self.animations[key][idx]

    def _sync_hitbox(self):
        self.hitbox.center = self.actor.pos

    def draw(self, screen, camera_x=0, camera_y=0):
        should_draw = True
        if self.invincible_timer > 0:
            if int(self.invincible_timer * 15) % 2 == 0:
                should_draw = False
        
        if should_draw:
            real_x = self.actor.x
            real_y = self.actor.y
            self.actor.x -= camera_x
            self.actor.y -= camera_y
            self.actor.draw()
            
            # Debug: Hitbox de ATAQUE (Azul)
            if self.state == "attack1":
                dbg_atk = self.attack_hitbox.copy()
                dbg_atk.x -= camera_x
                dbg_atk.y -= camera_y
                screen.draw.rect(dbg_atk, (0, 0, 255)) 
            
            self.actor.x = real_x
            self.actor.y = real_y

        # Debug Hitbox Corpo (Vermelho)
        self.hitbox.x -= camera_x
        self.hitbox.y -= camera_y
        # screen.draw.rect(self.hitbox, (255, 0, 0))
        self.hitbox.x += camera_x
        self.hitbox.y += camera_y