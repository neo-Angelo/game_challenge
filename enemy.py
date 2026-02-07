from pgzero.actor import Actor
from pygame import Rect
import math
import random

TILE_SIZE = 48 

class BaseEnemy:
    def __init__(self, x, y, image_prefix, speed=80):
        self.start_pos = (x, y) 
        self.image_prefix = image_prefix 
        self.speed = speed
        
        self.actor = Actor(f"enemies/{image_prefix}_idle_right_0", pos=(x, y))
        
        self.frame_timer = 0
        self.current_frame = 0
        
        # --- CONFIGURAÇÃO DE ANIMAÇÃO PADRÃO (Esqueleto) ---
        self.idle_frames = 4
        self.move_frames = 4 
        
        self.state = "idle"   
        self.direction = "right" 
        
        self.target_x = x
        self.target_y = y
        self.is_moving = False
        
        self.hitbox = Rect(0, 0, 50, 50) # Ajustei levemente a hitbox
        self.hitbox.center = self.actor.pos

        self.health = 4
        self.flash_timer = 0 
        
        # --- CONFIGURAÇÃO DE STUN PADRÃO ---
        self.stun_timer = 0
        self.stun_duration = 0.2 # Padrão (Esqueleto)

    def update(self, dt, map_width, map_height, player_pos):
        if self.flash_timer > 0:
            self.flash_timer -= dt

        # Lógica de Stun usando a variável duration
        if self.stun_timer > 0:
            self.stun_timer -= dt
            return 

        if self.is_moving:
            self.state = "move"
            self._move_smoothly(dt)
        else:
            self.state = "idle"
            self._ai_logic(dt, map_width, map_height, player_pos)
            
            px, py = player_pos
            # Olha para o player se estiver perto
            if abs(px - self.actor.x) < 200 and abs(py - self.actor.y) < 200:
                if px < self.actor.x: self.direction = "left"
                else: self.direction = "right"
            else:
                # Olha para onde anda
                if self.target_x < self.actor.x: self.direction = "left"
                elif self.target_x > self.actor.x: self.direction = "right"

        self.hitbox.center = self.actor.pos
        self._animate(dt)

    def take_damage(self, amount):
        self.health -= amount
        self.flash_timer = 0.2 
        # Usa a duração específica desse inimigo
        self.stun_timer = self.stun_duration 
        return self.health <= 0

    def _move_smoothly(self, dt):
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
        
        # Define quantos frames tem a ação atual
        limit = self.idle_frames
        if self.state == "move":
            limit = self.move_frames

        if self.frame_timer > 0.15: 
            self.frame_timer = 0
            # Garante que não puxe um frame que não existe
            self.current_frame = (self.current_frame + 1) % limit
            
            img_name = f"{self.image_prefix}_{self.state}_{self.direction}_{self.current_frame}"
            try:
                self.actor.image = f"enemies/{img_name}"
            except:
                pass

    def _ai_logic(self, dt, map_width, map_height, player_pos):
        pass

    def draw(self, screen, camera_x, camera_y):
        if self.flash_timer > 0 and (int(self.flash_timer * 20) % 2 == 0):
            pass 
        else:
            real_x, real_y = self.actor.pos
            self.actor.x -= camera_x
            self.actor.y -= camera_y
            self.actor.draw()
            
            # Hitbox Debug (Opcional)
            # self.hitbox.x -= camera_x
            # self.hitbox.y -= camera_y
            # screen.draw.rect(self.hitbox, (255, 0, 0))
            # self.hitbox.x += camera_x
            # self.hitbox.y += camera_y
            
            self.actor.pos = (real_x, real_y)


# --- ESQUELETO (Mantém o padrão) ---
class SmartEnemy(BaseEnemy):
    def __init__(self, x, y, image_prefix, speed=100): 
        super().__init__(x, y, image_prefix, speed)
        self.wait_timer = 0 
        self.detection_radius = 250
        self.patrol_radius = 200
        self.mode = "PATROL"

    def _ai_logic(self, dt, map_width, map_height, player_pos):
        # ... Lógica original do SmartEnemy ...
        if self.wait_timer > 0:
            self.wait_timer -= dt
            return

        px, py = player_pos
        dx = px - self.actor.x
        dy = py - self.actor.y
        dist_to_player = math.sqrt(dx**2 + dy**2)

        if dist_to_player < self.detection_radius:
            self.mode = "CHASE"
        else:
            self.mode = "PATROL"
        
        next_x = self.actor.x
        next_y = self.actor.y
        move_decided = False

        if self.mode == "CHASE":
            prefer_x = abs(dx) > abs(dy)
            if dx != 0 and dy != 0 and random.random() < 0.25:
                prefer_x = not prefer_x
            
            move_x = 0; move_y = 0
            if prefer_x:
                if dx != 0: move_x = TILE_SIZE if dx > 0 else -TILE_SIZE
                else: move_y = TILE_SIZE if dy > 0 else -TILE_SIZE
            else:
                if dy != 0: move_y = TILE_SIZE if dy > 0 else -TILE_SIZE
                else: move_x = TILE_SIZE if dx > 0 else -TILE_SIZE
            
            next_x += move_x
            next_y += move_y
            move_decided = True
            self.wait_timer = random.uniform(0.01, 0.05)

        elif self.mode == "PATROL":
            if random.random() < 0.02:
                self.wait_timer = random.uniform(1.0, 2.0)
                return

            directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
            dx, dy = random.choice(directions)
            
            possible_x = self.actor.x + (dx * TILE_SIZE)
            possible_y = self.actor.y + (dy * TILE_SIZE)
            
            start_x, start_y = self.start_pos
            dist_from_home = math.sqrt((possible_x - start_x)**2 + (possible_y - start_y)**2)
            
            if dist_from_home <= self.patrol_radius:
                next_x = possible_x
                next_y = possible_y
                move_decided = True
                self.wait_timer = random.uniform(0.5, 1.5)
            else:
                self.wait_timer = 0.5
                return

        if move_decided:
            margin = TILE_SIZE / 2
            if (margin <= next_x <= map_width - margin) and \
               (margin <= next_y <= map_height - margin):
                self.target_x = next_x
                self.target_y = next_y
                self.is_moving = True


# --- NOVA CLASSE: BRUXA ---
class WitchEnemy(SmartEnemy):
    def __init__(self, x, y, image_prefix, speed=130): # Speed padrão maior (era 100)
        super().__init__(x, y, image_prefix, speed)
        
        # CONFIGURAÇÕES ESPECÍFICAS DA BRUXA
        self.detection_radius = 400  # Vê muito mais longe (esqueleto é 250)
        self.stun_duration = 0.5     # Stun mais longo
        
        # Frames de animação específicos
        self.idle_frames = 4  # witch_idle_...0 a 3
        self.move_frames = 6  # witch_move_...0 a 5