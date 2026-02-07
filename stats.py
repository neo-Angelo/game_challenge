from pgzero.actor import Actor

class PlayerStats:
    def __init__(self, max_hp=5):
        self.max_hp = max_hp
        self.hp = max_hp
        self.is_dead = False

    def take_damage(self, amount):

        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.is_dead = True
            return True # Morreu
        return False

    def draw(self, screen, images):

        

        for i in range(self.max_hp):
            screen.blit("background", (10 + i * 35, 10))
        

        for i in range(self.hp):
            screen.blit("heart", (10 + i * 35, 10))