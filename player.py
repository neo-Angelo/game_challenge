from pgzero.actor import Actor
from pygame import Rect, transform
import math

class Player:
    def __init__(
        self,
        pos,
        total_frames,
        scale,
        speed,
        anim_speed,
        images
    ):
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

        # carrega animações já escaladas
        self.animations = self._load_animations()

        self.actor._surf = self.animations["idle_down"][0]

        # hitbox
        self.hitbox = Rect(0, 0, 32 * scale, 32 * scale)
        self._sync_hitbox()

    # ------------------------
    # Load animations (ESCALA REAL)
    # ------------------------
    def _load_animation(self, base_name):
        frames = []
        for i in range(self.total_frames):
            img = getattr(self.images, f"{base_name}_{i}")
            surf = transform.scale(
                img,
                (img.get_width() * self.scale, img.get_height() * self.scale)
            )
            frames.append(surf)
        return frames

    def _load_animations(self):
        anims = {}
        for state in ["idle", "run"]:
            for direction in ["up", "down", "left", "right"]:
                key = f"{state}_{direction}"
                anims[key] = self._load_animation(key)
        return anims

    # ------------------------
    # Update
    # ------------------------
    def update(self, dt, keyboard):
        self._move(dt, keyboard)
        self._animate(dt)
        self._sync_hitbox()

    # ------------------------
    # Movement
    # ------------------------
    def _move(self, dt, keyboard):
        dx = dy = 0

        if keyboard.a:
            dx -= 1
            self.direction = "left"
        elif keyboard.d:
            dx += 1
            self.direction = "right"

        if keyboard.w:
            dy -= 1
            self.direction = "up"
        elif keyboard.s:
            dy += 1
            self.direction = "down"

        if dx == 0 and dy == 0:
            self.state = "idle"
            return

        self.state = "run"

        if dx != 0 and dy != 0:
            length = math.sqrt(dx*dx + dy*dy)
            dx /= length
            dy /= length

        self.actor.x += dx * self.speed * dt
        self.actor.y += dy * self.speed * dt

    # ------------------------
    # Animation
    # ------------------------
    def _animate(self, dt):
        self.frame_timer += dt
        if self.frame_timer < self.anim_speed:
            return

        self.frame_timer = 0
        self.current_frame = (self.current_frame + 1) % self.total_frames

        key = f"{self.state}_{self.direction}"
        self.actor._surf = self.animations[key][self.current_frame]

    # ------------------------
    # Hitbox
    # ------------------------
    def _sync_hitbox(self):
        self.hitbox.center = self.actor.pos

    # ------------------------
    # Draw
    # ------------------------
    def draw(self):
        self.actor.draw()

