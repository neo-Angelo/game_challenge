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
        
        # Hitbox (60x60)
        self.hitbox = Rect(0, 0, 60, 60)
        self.hitbox.center = self.actor.pos

        # --- NOVO: Vida do Inimigo ---
        self.health = 4
        # Timer visual para piscar quando tomar dano (igual ao player)
        self.flash_timer = 0 

    def update(self, dt, map_width, map_height, player_pos):
        # Gerencia o piscar de dano
        if self.flash_timer > 0:
            self.flash_timer -= dt

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

    def take_damage(self, amount):
        """Reduz a vida. Retorna True se morreu."""
        self.health -= amount
        self.flash_timer = 0.2 # Pisca branco por 0.2s
        return self.health <= 0

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
        # Lógica de piscar ao tomar dano (opcional, mas visualmente bom)
        if self.flash_timer > 0 and (int(self.flash_timer * 20) % 2 == 0):
            # Pula o desenho para piscar
            pass 
        else:
            real_x, real_y = self.actor.pos
            self.actor.x -= camera_x
            self.actor.y -= camera_y
            self.actor.draw()
            
            # Hitbox Vermelha
            self.hitbox.x -= camera_x
            self.hitbox.y -= camera_y
            screen.draw.rect(self.hitbox, (255, 0, 0))
            self.hitbox.x += camera_x
            self.hitbox.y += camera_y
            
            self.actor.pos = (real_x, real_y)

# --- CLASSES FILHAS (Mantêm-se iguais, só copiei o cabeçalho) ---
class RoamingEnemy(BaseEnemy):
    # (Seu código original aqui...)
    pass

class ChasingEnemy(BaseEnemy):
    # (Seu código original aqui...)
    # Certifique-se de que ChasingEnemy herda o __init__ ou chama super().__init__ 
    # para ter self.health
    def __init__(self, x, y, image_prefix, speed=110): 
        super().__init__(x, y, image_prefix, speed)
        self.wait_timer = 0 
        # Resto do código da IA...
    
    # Copie o método _ai_logic que fizemos na resposta anterior
    def _ai_logic(self, dt, map_width, map_height, player_pos):
        # (Código da IA que fizemos anteriormente)
        if self.wait_timer > 0:
            self.wait_timer -= dt
            return

        if random.random() < 0.02:
            self.wait_timer = random.uniform(0.5, 1.5)
            return

        px, py = player_pos
        dx = px - self.actor.x
        dy = py - self.actor.y
        move_x = 0
        move_y = 0
        prefer_x = abs(dx) > abs(dy)
        if dx != 0 and dy != 0 and random.random() < 0.25:
            prefer_x = not prefer_x

        if prefer_x:
            if dx != 0: move_x = TILE_SIZE if dx > 0 else -TILE_SIZE
            else: move_y = TILE_SIZE if dy > 0 else -TILE_SIZE
        else:
            if dy != 0: move_y = TILE_SIZE if dy > 0 else -TILE_SIZE
            else: move_x = TILE_SIZE if dx > 0 else -TILE_SIZE
            
        next_x = self.actor.x + move_x
        next_y = self.actor.y + move_y
        
        margin = TILE_SIZE / 2
        if (margin <= next_x <= map_width - margin) and \
           (margin <= next_y <= map_height - margin):
            self.target_x = next_x
            self.target_y = next_y
            self.is_moving = True
            self.wait_timer = random.uniform(0.01, 0.05)