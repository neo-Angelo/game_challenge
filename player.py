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

        self.state = "idle"
        self.direction = "down"

        self.current_frame = 0
        self.frame_timer = 0

        self.actor = Actor("idle_down_0", pos=pos)
        
        self.target_x = self.actor.x
        self.target_y = self.actor.y
        self.is_moving = False

        self.animations = self._load_animations()
        self.actor._surf = self.animations["idle_down"][0]

        hitbox_size = 30
        self.hitbox = Rect(0, 0, hitbox_size, hitbox_size)
        self._sync_hitbox()
        
        # --- NOVO: Timer de Invencibilidade ---
        self.invincible_timer = 0

    def _load_animation(self, base_name):
        frames = []
        for i in range(self.total_frames):
            img = getattr(self.images, f"{base_name}_{i}")
            frames.append(img)
        return frames

    def _load_animations(self):
        anims = {}
        for state in ["idle", "run"]:
            for direction in ["up", "down", "left", "right"]:
                key = f"{state}_{direction}"
                anims[key] = self._load_animation(key)
        return anims

    def update(self, dt, keyboard, map_width, map_height):
        # 1. Diminui timer de invencibilidade
        if self.invincible_timer > 0:
            self.invincible_timer -= dt

        if self.is_moving:
            self._continue_moving(dt)

        if not self.is_moving:
            self._check_input(keyboard, map_width, map_height)
            
        self._animate(dt)
        self._sync_hitbox()

    # --- NOVO: Função para tomar dano ---
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
        if self.frame_timer < self.anim_speed:
            return

        self.frame_timer = 0
        self.current_frame = (self.current_frame + 1) % self.total_frames

        key = f"{self.state}_{self.direction}"
        if key in self.animations:
            self.actor._surf = self.animations[key][self.current_frame]

    def _sync_hitbox(self):
        self.hitbox.center = self.actor.pos

    def draw(self, screen, camera_x=0, camera_y=0):
        # --- LÓGICA DE PISCAR ---
        # Se estiver invencível, pisca rápido
        should_draw = True
        if self.invincible_timer > 0:
            # Multiplicamos por 15 para definir a velocidade da piscada
            # O operador % 2 faz alternar entre 0 e 1 (visível e invisível)
            if int(self.invincible_timer * 15) % 2 == 0:
                should_draw = False # Pula o desenho neste frame
        
        if should_draw:
            real_x = self.actor.x
            real_y = self.actor.y
            
            self.actor.x -= camera_x
            self.actor.y -= camera_y
            
            self.actor.draw()
            
            # Restaura posição real
            self.actor.x = real_x
            self.actor.y = real_y

        # Debug Hitbox (Desenha sempre, mesmo piscando, pra vc ver onde está)
        self.hitbox.x -= camera_x
        self.hitbox.y -= camera_y
        
        # screen.draw.rect(self.hitbox, (255, 0, 0))
        
        self.hitbox.x += camera_x
        self.hitbox.y += camera_y