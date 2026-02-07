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
        self.total_frames = 4 
        self.state = "idle"   
        self.direction = "right" 
        
        self.target_x = x
        self.target_y = y
        self.is_moving = False
        
        # --- MUDANÇA 1: Hitbox reduzida para 2x (60px) ---
        # Antes 90, agora 60 (para ser 2x a base de 30)
        self.hitbox = Rect(0, 0, 40, 40)
        self.hitbox.center = self.actor.pos

    def update(self, dt, map_width, map_height, player_pos):
        if self.is_moving:
            self.state = "move"
            self._move_smoothly(dt)
        else:
            self.state = "idle"
            self._ai_logic(dt, map_width, map_height, player_pos)
            
            px, py = player_pos
            if px < self.actor.x:
                self.direction = "left"
            else:
                self.direction = "right"

        self.hitbox.center = self.actor.pos
        self._animate(dt, images=None)

    def _move_smoothly(self, dt):
        step = self.speed * dt
        diff_x = self.target_x - self.actor.x
        diff_y = self.target_y - self.actor.y
        dist = math.sqrt(diff_x**2 + diff_y**2)

        if diff_x < 0: self.direction = "left"
        elif diff_x > 0: self.direction = "right"

        if dist <= step:
            self.actor.x = self.target_x
            self.actor.y = self.target_y
            self.is_moving = False
        else:
            self.actor.x += (diff_x / dist) * step
            self.actor.y += (diff_y / dist) * step

    def _animate(self, dt, images):
        self.frame_timer += dt
        if self.frame_timer > 0.15: 
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % self.total_frames
            
            img_name = f"{self.image_prefix}_{self.state}_{self.direction}_{self.current_frame}"
            try:
                self.actor.image = f"enemies/{img_name}"
            except:
                pass

    def _ai_logic(self, dt, map_width, map_height, player_pos):
        pass

    def draw(self, screen, camera_x, camera_y):
        real_x, real_y = self.actor.pos
        self.actor.x -= camera_x
        self.actor.y -= camera_y
        self.actor.draw()
        
        self.hitbox.x -= camera_x
        self.hitbox.y -= camera_y
        screen.draw.rect(self.hitbox, (255, 0, 0))
        self.hitbox.x += camera_x
        self.hitbox.y += camera_y
        
        self.actor.pos = (real_x, real_y)


# --- INIMIGO DE PERSEGUIÇÃO ATUALIZADO ---
class ChasingEnemy(BaseEnemy):
    def __init__(self, x, y, image_prefix, speed=110): 
        super().__init__(x, y, image_prefix, speed)
        self.wait_timer = 0 

    def _ai_logic(self, dt, map_width, map_height, player_pos):
        # 1. Delay
        if self.wait_timer > 0:
            self.wait_timer -= dt
            return

        # 2% de chance de parar para descansar
        if random.random() < 0.02:
            self.wait_timer = random.uniform(0.5, 1.5)
            return

        # 2. Calcula Distância
        px, py = player_pos
        dx = px - self.actor.x
        dy = py - self.actor.y
        
        move_x = 0
        move_y = 0
        
        # --- MUDANÇA 2: "Destoar" o caminho (Ruído na decisão) ---
        # Por padrão, escolhemos o eixo com maior distância (Lógica Gulosa)
        prefer_x = abs(dx) > abs(dy)
        
        # MAS, temos 25% de chance de tentar ir pelo outro eixo (se possível)
        # Isso faz alguns inimigos irem por cima e outros por baixo (Zigue-Zague)
        if dx != 0 and dy != 0 and random.random() < 0.25:
            prefer_x = not prefer_x

        # Aplica a decisão
        if prefer_x:
            if dx != 0:
                move_x = TILE_SIZE if dx > 0 else -TILE_SIZE
            else:
                move_y = TILE_SIZE if dy > 0 else -TILE_SIZE
        else:
            if dy != 0:
                move_y = TILE_SIZE if dy > 0 else -TILE_SIZE
            else:
                move_x = TILE_SIZE if dx > 0 else -TILE_SIZE
            
        # Define destino
        next_x = self.actor.x + move_x
        next_y = self.actor.y + move_y
        
        # Verifica limites
        margin = TILE_SIZE / 2
        if (margin <= next_x <= map_width - margin) and \
           (margin <= next_y <= map_height - margin):
            
            self.target_x = next_x
            self.target_y = next_y
            self.is_moving = True
            
            # Pequeno delay aleatório entre passos para dessincronizar movimento
            self.wait_timer = random.uniform(0.01, 0.05)