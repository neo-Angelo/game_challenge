from player import Player

WIDTH = 800
HEIGHT = 600

player = Player(
    pos=(WIDTH // 2, HEIGHT // 2),
    total_frames=8,
    scale=3,          # 🔥 agora funciona de verdade
    speed=200,
    anim_speed=0.1,
    images=images
)

def update(dt):
    player.update(dt, keyboard)

def draw():
    screen.clear()
    player.draw()

